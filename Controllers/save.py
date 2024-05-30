from starlette.responses import RedirectResponse

from DTO.PrincipalController import principal
from PostgreSQL_DB_setup.session_funcs import delete_calc_by_calc_id
from PostgreSQL_DB_setup.tables import Calcs, SharedCalcsWithAll, SharedCalcsWithFew
from Controllers.get import get_current_user_id, user_if_exist


def current_user_calc_redirect(db_session, user_inputs, current_user_email):
    principal.calculate(user_inputs)
    current_user_id = get_current_user_id(current_user_email, db_session)

    calc_to_save = Calcs(house_price=principal.user_inputs['house_price'],
                         down_payment=principal.user_inputs['down_payment'],
                         bond_price=principal.user_inputs['bond_price'],
                         bank_name=principal.user_inputs['dropdown'],
                         principal_value=principal.principal,
                         capital_loss=principal.capital_loss,
                         user_id=current_user_id
                         )
    db_session.add(calc_to_save)
    db_session.commit()

    return RedirectResponse(url="/logged_in")


def changes_to_calc_redirect(db_session, user_inputs):
    principal.calculate(user_inputs)
    updated_values = {'house_price': principal.user_inputs['house_price'],
                      'down_payment': principal.user_inputs['down_payment'],
                      'bond_price': principal.user_inputs['bond_price'],
                      'bank_name': principal.user_inputs['dropdown'],
                      'principal_value': principal.principal,
                      'capital_loss': principal.capital_loss
                      }
    # overwrite calc in db
    db_session.query(Calcs).filter(Calcs.calc_id == user_inputs['calc_id']).update(updated_values)
    db_session.commit()

    return RedirectResponse(url="/logged_in")


def new_access_level_redirect(db_session, user_inputs):
    print('\n\nnew_access_level_redirect:')
    print('user_inputs: ', user_inputs)


    selected_user = user_if_exist(db_session, user_inputs['email_shared_with'])

    print('selected_user: ', selected_user)

    if user_inputs['action'] == 'Gem ændringer':
        updated_values = {'access_level': user_inputs['new_access_level']}

        if user_inputs['email_shared_with'] == 'alle brugere':
            (db_session.query(SharedCalcsWithAll).filter(SharedCalcsWithAll.calc_id == user_inputs['calc_id'])
             .update(updated_values))
        else:
            (db_session.query(SharedCalcsWithFew).filter(SharedCalcsWithFew.calc_id == user_inputs['calc_id'],
                                                         SharedCalcsWithFew.user_id == selected_user.user_id
                                                         ).update(updated_values))
        db_session.commit()

    if user_inputs['action'] == 'Stop deling':
        if user_inputs['email_shared_with'] == 'alle brugere':
            delete_calc_by_calc_id(db_session, SharedCalcsWithAll, user_inputs['calc_id'])
        else:
            calc_to_delete = (db_session.query(SharedCalcsWithFew)
                              .filter(SharedCalcsWithFew.calc_id == user_inputs['calc_id'],
                                      SharedCalcsWithFew.user_id == selected_user.user_id
                                      )
                              .one())
            db_session.delete(calc_to_delete)
            db_session.commit()

    return RedirectResponse(url="/logged_in")
