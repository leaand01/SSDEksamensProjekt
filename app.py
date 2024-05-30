from typing import Dict

from fastapi import Depends, Request, FastAPI

from starlette.middleware.sessions import SessionMiddleware
from starlette.responses import RedirectResponse, Response

from sqlalchemy.orm import Session

from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from Middleware.validate_user_inputs import validate_user_inputs
from Middleware import rate_limiter
from Middleware.getters import get_db, get_current_user
from Controllers import edit, get, save, share
from Controllers.view_redirects import views
from PostgreSQL_DB_setup.init_db import init_db
from Google_login import auth
import config


init_db()
limiter = rate_limiter.limiter
app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.middleware("http")
async def middleware_wrapper(request: Request, call_next):
    return await validate_user_inputs(request, call_next)

app.add_middleware(SessionMiddleware, secret_key=config.secret_key_for_signing_session_cookie)


@app.get('/')
@limiter.limit(config.slow_api_rate_limit)
async def login_button(request: Request):
    return views.TemplateResponse('login_with_google.html', {'request': request})


@app.get('/login')
async def google_login(request: Request):
    return await auth.google_login(request)


@app.get("/auth")
async def google_callback(request: Request, db_session: Session = Depends(get_db)):
    return await auth.google_callback(request, db_session)


@app.api_route('/logged_in', methods=['GET', 'POST'])
@limiter.limit(config.slow_api_rate_limit)
async def logged_in(request: Request, current_user_email: Dict = Depends(get_current_user), db_session: Session = Depends(get_db)):
    user_inputs = await get.user_inputs(request)
    return get.logged_in_redirect(request, db_session, current_user_email, user_inputs)


@app.post('/save_calc')
@limiter.limit(config.slow_api_rate_limit)
async def save_calc(request: Request, current_user_email: Dict = Depends(get_current_user), db_session: Session = Depends(get_db)):
    user_inputs = request.state.form_data
    return save.current_user_calc_redirect(db_session, user_inputs, current_user_email)


@app.post('/edit_calc')
@limiter.limit(config.slow_api_rate_limit)
async def edit_calc(request: Request, current_user_email: Dict = Depends(get_current_user), db_session: Session = Depends(get_db)):
    user_inputs = request.state.form_data
    return edit.calc_redirect(request, db_session, user_inputs)


@app.post('/save_changes_to_calc')
@limiter.limit(config.slow_api_rate_limit)
async def save_changes_to_calc(request: Request, current_user_email: Dict = Depends(get_current_user), db_session: Session = Depends(get_db)):
    user_inputs = request.state.form_data
    return save.changes_to_calc_redirect(db_session, user_inputs)


@app.post('/share_calc')
@limiter.limit(config.slow_api_rate_limit)
async def share_calc(request: Request, current_user_email: Dict = Depends(get_current_user), db_session: Session = Depends(get_db)):
    user_inputs = request.state.form_data
    return share.calc_values_redirect(request, db_session, user_inputs)


@app.post('/share_with_single_user')
@limiter.limit(config.slow_api_rate_limit)
async def share_with_selected_user(request: Request, current_user_email: Dict = Depends(get_current_user), db_session: Session = Depends(get_db)):
    user_inputs = request.state.form_data
    return share.calc_with_user_redirect(request, db_session, user_inputs)


@app.post('/share_with_all_users')
@limiter.limit(config.slow_api_rate_limit)
async def share_with_all(request: Request, current_user_email: Dict = Depends(get_current_user), db_session: Session = Depends(get_db)):
    user_inputs = request.state.form_data
    return share.calc_with_all_users_redirect(db_session, user_inputs, current_user_email)


@app.post('/edit_sharing_access')
@limiter.limit(config.slow_api_rate_limit)
async def edit_sharing_access(request: Request, current_user_email: Dict = Depends(get_current_user), db_session: Session = Depends(get_db)):
    user_inputs = request.state.form_data
    return edit.shared_calc_redirect(request, db_session, user_inputs)


@app.post('/update_sharing_access')
@limiter.limit(config.slow_api_rate_limit)
async def save_updated_sharing_access(request: Request, current_user_email: Dict = Depends(get_current_user), db_session: Session = Depends(get_db)):
    user_inputs = request.state.form_data
    return save.new_access_level_redirect(db_session, user_inputs)


@app.post('/delete_calc')
@limiter.limit(config.slow_api_rate_limit)
async def delete_calc(request: Request, current_user_email: Dict = Depends(get_current_user), db_session: Session = Depends(get_db)):
    user_inputs = request.state.form_data
    return edit.delete_calc_redirect(db_session, user_inputs)


@app.get('/logout')
@limiter.limit(config.slow_api_rate_limit)
async def logout(request: Request, response: Response, current_user_email: Dict = Depends(get_current_user)):
    request.session.clear()
    response.delete_cookie(key='session')
    return RedirectResponse(url="/")
