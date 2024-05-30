from fastapi import Request
from starlette.responses import RedirectResponse

import config
from DTO.DropDownBankNamesController import dropdown_bank_names
from DTO.PrincipalController import principal
from PostgreSQL_DB_setup.session_funcs import delete_shared_calcs
from PostgreSQL_DB_setup.tables import SharedCalcsWithFew, SharedCalcsWithAll
from Controllers import get
from Controllers.view_redirects import views


def calc_values_redirect(request: Request, db_session, user_inputs):
    # load calc values to share
    calc_values_as_dict = get.calc_values(db_session, user_inputs)
    principal.calculate(calc_values_as_dict)

    context = {'request': request,
               'dropdown_bank_names': dropdown_bank_names,
               'input_house_price': principal.user_inputs['house_price'],
               'input_down_payment': principal.user_inputs['down_payment'],
               'input_bond_price': principal.user_inputs['bond_price'],
               'selected_bank': principal.user_inputs['dropdown'],
               'principal_value': principal.principal,
               'capital_loss': principal.capital_loss,
               'list_access_levels': config.list_access_levels,
               'calc_id': user_inputs['calc_id']
               }
    return views.TemplateResponse('share_calc.html', context)


def calc_with_user_redirect(request: Request, db_session, user_inputs):
    print('calc_with_user_redirect:')

    existing_user = get.user_if_exist(db_session, user_inputs['share_with_single_user'])

    print('existing_user: ', existing_user)

    if existing_user is None:
        response_string = 'Hvis den indtastede email er i databasen, er din beregning nu delt.'
        return views.TemplateResponse('invalid_input.html', {'request': request, 'response_string': response_string})

    else:
        try:
            print('adding to sharedcalcsWithFew')
            print(f'calc_id {user_inputs["calc_id"]}, user_id {existing_user.user_id}, access_level {user_inputs["single_user_access_level"]}')
            shared_calc_few = SharedCalcsWithFew(calc_id=user_inputs['calc_id'],
                                                 user_id=existing_user.user_id,
                                                 access_level=user_inputs['single_user_access_level'],
                                                 )
            db_session.add(shared_calc_few)
            db_session.commit()
        except Exception as e:
            db_session.rollback()
            print(f"Rolled back due to Exception: {e}")
            print('The calc is already shared with the user. Sharing attempt is rolled back.')

    return RedirectResponse(url="/logged_in")


def calc_with_all_users_redirect(db_session, user_inputs, current_user):
    current_user_id = get.get_current_user_id(current_user, db_session)

    try:
        # step1: share calc with yourself (event.listener will share with all other users)
        calc_to_share_with_all = SharedCalcsWithAll(calc_id=user_inputs['calc_id'],
                                                    user_id=current_user_id,
                                                    access_level=user_inputs['all_users_access_level']
                                                    )
        db_session.add(calc_to_share_with_all)
        db_session.commit()
    except Exception as e:
        db_session.rollback()
        print(f"Rolled back due to Exception: {e}")
        print('Step1 in adding calc to SharedCalcsWithAll failed')

    try:
        # step2: Delete shared calc with yourself
        delete_shared_calcs(session=db_session,
                            calc_id=user_inputs['calc_id'],
                            user_id=current_user_id
                            )
    except Exception as e:
        db_session.rollback()
        print(f"Rolled back due to Exception: {e}")
        print('Step2 in adding calc to SharedCalcsWithAll failed')

    return RedirectResponse(url="/logged_in")
