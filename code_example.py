from Controllers.get import get_current_user_id
from Cryptography.encryption_funcs import crypto
from Middleware.getters import temp_deactivate_event_listener
from PostgreSQL_DB_setup.init_db import init_db
from PostgreSQL_DB_setup.tables import Users

from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker

import config
from PostgreSQL_DB_setup.tables import SharedCalcsWithAll
from PostgreSQL_DB_setup.session_funcs import share_with_all_users


print('init_db')
init_db()

print('create engine')
engine = create_engine(config.postgresql_db_url)
session = sessionmaker(bind=engine)
db_session = session()
event.listen(SharedCalcsWithAll, 'after_insert', share_with_all_users)


print('add new user')
new_user_email = 'andersenlea85@gmail.com'

encrypted_email = crypto.encrypt(new_user_email)
db_session.add(Users(email=encrypted_email))
db_session.commit()

print('deactivae event listener')
event.remove(SharedCalcsWithAll, 'after_insert', share_with_all_users)  # deactivate

from sqlalchemy import distinct

print('share calcs')
# share SharedCalcsWIthALL with new user
new_user_id = get_current_user_id(encrypted_email, db_session)

# unique_all_shared_calcs = db_session.query(SharedCalcsWithAll).filter(SharedCalcsWithAll.calc_id.distinct()).all()
unique_all_shared_calcs_ids = db_session.query(SharedCalcsWithAll.calc_id.distinct()).all()
unique_all_shared_calcs_ids = [calc_id for calc_id, in  unique_all_shared_calcs_ids]
print('unique_all_shared_calcs_ids: ', unique_all_shared_calcs_ids)

unique_all_shared_calcs = db_session.query(SharedCalcsWithAll).filter(SharedCalcsWithAll.calc_id.in_(unique_all_shared_calcs_ids)).all()
print('unique_all_shared_calcs: ', unique_all_shared_calcs)



calcs_shared_with_all = []
for calc in unique_all_shared_calcs:
    c = SharedCalcsWithAll(calc_id=calc.calc_id, user_id=new_user_id, access_level=calc.access_level)  # share calc with new user without event.listener
    calcs_shared_with_all.append(c)

db_session.add_all(calcs_shared_with_all)
db_session.commit()

print('reactivate event listener')
# re-activate event.listener
event.listen(SharedCalcsWithAll, 'after_insert', share_with_all_users)


print('close session')
db_session.close()

print('done')




# placering måske Controllers.share # NÅETHERTIL TODO
def existing_calcs_with_new_user(encrypted_email):
    """Share all calcs in SharedCalcsWithAll with new user by deactivating the event listener within while statement"""
    with temp_deactivate_event_listener():
        unique_all_shared_calc_ids = db_session.query(SharedCalcsWithAll.calc_id.distinct()).all()
        unique_all_shared_calc_ids = [calc_id for calc_id, in unique_all_shared_calc_ids]

        unique_all_shared_calcs = (db_session.query(SharedCalcsWithAll)
                                   .filter(SharedCalcsWithAll.calc_id.in_(unique_all_shared_calc_ids)).all())

        new_user_id = get_current_user_id(encrypted_email, db_session)
        calcs_shared_with_all = []
        for calc in unique_all_shared_calcs:
            c = SharedCalcsWithAll(calc_id=calc.calc_id, user_id=new_user_id, access_level=calc.access_level)
            calcs_shared_with_all.append(c)

        db_session.add_all(calcs_shared_with_all)
        db_session.commit()
