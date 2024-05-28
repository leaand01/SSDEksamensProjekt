from sqlalchemy import create_engine, event, inspect
from sqlalchemy.orm import sessionmaker

import config
from Cryptography.encryption_funcs import crypto
from PostgreSQL_DB_setup.tables import Base, Users, Calcs, SharedCalcsWithAll
from PostgreSQL_DB_setup.session_funcs import share_with_all_users, delete_shared_calcs


def init_db():
    """Initialize local database if it does not exist"""
    # Setup database
    engine = create_engine(config.postgresql_db_url)

    inspector = inspect(engine)
    if (not inspector.has_table('users')
            or not inspector.has_table('calcs')
            or not inspector.has_table('sharedCalcsWithAll')
            or not inspector.has_table('sharedCalcsWithFew')
        ):
        Base.metadata.create_all(engine)
        session = sessionmaker(bind=engine)
        # Session = sessionmaker(bind=engine)

        event.listen(SharedCalcsWithAll, 'after_insert', share_with_all_users)  # forsøg
        session = session()
        # session = Session()

        # Create user with shared calcs
        user1 = Users(email=crypto.encrypt('nobody@gmail.com'))
        user2 = Users(email=crypto.encrypt('noone@gmail.com'))

        session.add_all([user1, user2])
        session.commit()

        # Create calculations
        calc1 = Calcs(house_price='500000', down_payment='100000', bond_price='97', bank_name='Totalkredit',
                      principal_value='442105', capital_loss='22105', user_id=user1.user_id)

        calc2 = Calcs(house_price='800000', down_payment='160000', bond_price='94', bank_name='RealkreditDanmark',
                      principal_value='715217', capital_loss='57217', user_id=user1.user_id)

        calc3 = Calcs(house_price='1000000', down_payment='50000', bond_price='99', bank_name='RealkreditDanmark',
                      principal_value='997938', capital_loss='29938',
                      user_id=user2.user_id)

        calc4 = Calcs(house_price='750000', down_payment='150000', bond_price='95', bank_name='RealkreditDanmark',
                      principal_value='664516', capital_loss='46516',
                      user_id=user2.user_id)

        session.add_all([calc1, calc2, calc3, calc4])
        session.commit()

        # # forsøg ny tabel
        # calc1_share_all = SharedCalcsWithAll(calc_id=calc1.calc_id, access_level='read_only')
        # calc2_share_all = SharedCalcsWithAll(calc_id=calc2.calc_id, access_level='write')
        # calc3_share_all = SharedCalcsWithAll(calc_id=calc3.calc_id, access_level='write')
        #
        # session.add_all([calc1_share_all, calc2_share_all, calc3_share_all])
        # session.commit()

        # share all user1 calcs with all (first share with himself)
        calc1_share_all = SharedCalcsWithAll(calc_id=calc1.calc_id, user_id=user1.user_id, access_level='read_only')
        calc2_share_all = SharedCalcsWithAll(calc_id=calc2.calc_id, user_id=user1.user_id, access_level='write')
        # share one calc of user2 with all
        calc3_share_all = SharedCalcsWithAll(calc_id=calc3.calc_id, user_id=user2.user_id, access_level='write')

        session.add_all([calc1_share_all, calc2_share_all, calc3_share_all])
        session.commit()

        # Delete shared calculations with yourself
        delete_shared_calcs(session, calc1.calc_id, user1.user_id)
        delete_shared_calcs(session, calc2.calc_id, user1.user_id)
        delete_shared_calcs(session, calc3.calc_id, user2.user_id)

        session.close()
