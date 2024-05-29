import secrets
from contextlib import asynccontextmanager

from fastapi_sso.sso.google import GoogleSSO
from fastapi import Request, Depends, HTTPException

from sqlalchemy.orm import Session

from starlette.responses import RedirectResponse

import config
from Controllers.get import get_current_user_id
from Cryptography.encryption_funcs import crypto
from PostgreSQL_DB_setup.tables import Users, SharedCalcsWithAll
from Middleware.getters import get_db, temp_deactivate_event_listener
from Middleware.rate_limiter import limiter
from Controllers import get


@asynccontextmanager
async def get_google_sso():
    google_sso = GoogleSSO(**config.google_sso)
    yield google_sso


@limiter.limit(config.slow_api_rate_limit)
async def google_login(request: Request):
    """Login with Google account"""
    async with get_google_sso() as google_sso:
        state = secrets.token_urlsafe(32)
        request.session['state'] = state

        return await google_sso.get_login_redirect(redirect_uri=request.url_for("google_callback"),
                                                   params={"prompt": "login"},
                                                   state=state
                                                   )


@limiter.limit(config.slow_api_rate_limit)
async def google_callback(request: Request, db_session: Session = Depends(get_db)):
    """Process login response from Google and return user info"""
    async with get_google_sso() as google_sso:
        stored_state = request.session.pop('state', None)
        received_state = request.query_params.get("state")

        if stored_state != received_state:
            raise HTTPException(status_code=400, detail="State parameters do not match")

        user = await google_sso.verify_and_process(request)

        # if user do not exist
        existing_user = get.user_if_exist(db_session, user.email)
        if existing_user is None:
            encrypted_email = crypto.encrypt(user.email)
            db_session.add(Users(email=encrypted_email))
            db_session.commit()

            request.session['user_email'] = encrypted_email

            share_existing_calcs_with_new_user(encrypted_email, db_session)

        # if user exist
        else:
            existing_encrypted_email = existing_user.email
            request.session['user_email'] = existing_encrypted_email

        return RedirectResponse(url="/logged_in")


def share_existing_calcs_with_new_user(new_user_email, db_session):
    """Share all calcs in SharedCalcsWithAll with new user by deactivating the event listener within while statement"""
    with temp_deactivate_event_listener():
        unique_all_shared_calc_ids = db_session.query(SharedCalcsWithAll.calc_id.distinct()).all()
        unique_all_shared_calc_ids = [calc_id for calc_id, in unique_all_shared_calc_ids]

        unique_all_shared_calcs = (db_session.query(SharedCalcsWithAll)
                                   .filter(SharedCalcsWithAll.calc_id.in_(unique_all_shared_calc_ids)).all())

        new_user_id = get_current_user_id(new_user_email, db_session)
        calcs_shared_with_all = []
        for calc in unique_all_shared_calcs:
            c = SharedCalcsWithAll(calc_id=calc.calc_id, user_id=new_user_id, access_level=calc.access_level)
            calcs_shared_with_all.append(c)

        db_session.add_all(calcs_shared_with_all)
        db_session.commit()
