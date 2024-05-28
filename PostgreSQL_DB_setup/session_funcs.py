from sqlalchemy.orm import Session

from PostgreSQL_DB_setup.tables import Users, SharedCalcsWithAll


def share_with_all_users(mapper, connection, target):
    """Share calculation with all users by sharing it with yourself in table SharedCalcsWithAll"""
    session = Session(bind=connection)
    users = session.query(Users).all()
    for user in users:
        shared_entry = SharedCalcsWithAll(calc_id=target.calc_id, user_id=user.user_id,
                                          access_level=target.access_level)
        session.merge(shared_entry)
    session.commit()


def delete_shared_calcs(session, calc_id, user_id):
    """Delete the calculations shared with yourself in SharedCalcsWithAll so this table only show calculations shared
    with all users besides the user himself"""
    shared_calcs_to_delete = session.query(SharedCalcsWithAll).filter_by(calc_id=calc_id, user_id=user_id).all()
    for shared_calc in shared_calcs_to_delete:
        session.delete(shared_calc)
    session.commit()


def delete_calc_by_calc_id(session, table, calc_id):
    """Delete the calculations shared with yourself in SharedCalcsWIthAll so this table only show calculations shared
    with all users besides the user himself"""
    shared_calcs_to_delete = session.query(table).filter_by(calc_id=calc_id).all()
    for shared_calc in shared_calcs_to_delete:
        session.delete(shared_calc)
    session.commit()
