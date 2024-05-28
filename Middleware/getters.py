from fastapi import Request, HTTPException

from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, Session

from contextlib import contextmanager

import config
from PostgreSQL_DB_setup.tables import SharedCalcsWithAll
from PostgreSQL_DB_setup.session_funcs import share_with_all_users


def get_current_user(request: Request):
    user = request.session.get('user_email')  # return None if no user
    if user:
        return user
    else:
        raise HTTPException(status_code=401, detail='not authenticated. Access denied - you are not logged in.')


def get_db() -> Session:
    engine = create_engine(config.postgresql_db_url)
    session = sessionmaker(bind=engine)

    db_session = session()
    add_event_listener()

    try:
        yield db_session
    finally:
        db_session.close()


@contextmanager
def temp_deactivate_event_listener():
    remove_event_listener()
    try:
        yield
    finally:
        add_event_listener()


def add_event_listener():
    event.listen(SharedCalcsWithAll, 'after_insert', share_with_all_users)

def remove_event_listener():
    event.remove(SharedCalcsWithAll, 'after_insert', share_with_all_users)
