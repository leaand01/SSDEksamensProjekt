from fastapi import Request

from starlette.responses import RedirectResponse

import config
from DTO.DropDownBankNamesController import dropdown_bank_names
from DTO.PrincipalController import principal
from PostgreSQL_DB_setup.tables import Calcs
from Controllers import get
from Controllers.view_redirects import views


def calc_redirect(request: Request, db_session, user_inputs):
    # if pressed beregn in edit_calc
    if 'house_price' in user_inputs.keys():
        principal.calculate(user_inputs)

    # load calc values to edit
    else:
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
               'calc_id': user_inputs['calc_id']
               }
    return views.TemplateResponse('edit_calc.html', context)


def shared_calc_redirect(request: Request, db_session, user_inputs):
    shared_calc_details = db_session.query(Calcs).filter(Calcs.calc_id == user_inputs['calc_id']).one()

    context = {'request': request,
               'dropdown_bank_names': dropdown_bank_names,
               'input_house_price': shared_calc_details.house_price,
               'input_down_payment': shared_calc_details.down_payment,
               'input_bond_price': shared_calc_details.bond_price,
               'selected_bank': shared_calc_details.bank_name,
               'principal_value': shared_calc_details.principal_value,
               'capital_loss': shared_calc_details.capital_loss,
               'input_selected_access_level': user_inputs['access_level'],
               'shared_with': user_inputs['email_shared_with'],
               'list_access_levels': config.list_access_levels,
               'calc_id': user_inputs['calc_id']
               }
    return views.TemplateResponse('edit_sharing_access.html', context)


def delete_calc_redirect(db_session, user_inputs):
    calc_to_delete = db_session.query(Calcs).filter(Calcs.calc_id == user_inputs['calc_id']).one()
    db_session.delete(calc_to_delete)
    db_session.commit()

    return RedirectResponse(url="/logged_in")
