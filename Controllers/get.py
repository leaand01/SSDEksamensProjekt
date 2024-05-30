from typing import Dict

from fastapi import Request
from sqlalchemy import asc

from Cryptography.encryption_funcs import crypto
from DTO.DropDownBankNamesController import dropdown_bank_names
from DTO.PrincipalController import principal
from PostgreSQL_DB_setup.tables import Users, Calcs, SharedCalcsWithAll, SharedCalcsWithFew
from Controllers.view_redirects import views


async def user_inputs(request: Request):
    if request.method == 'POST':
        user_inputs = request.state.form_data  # Access the cached form data from the Middleware validators
    else:
        user_inputs = await request.form()
        user_inputs = dict(user_inputs)

    return user_inputs


def logged_in_redirect(request: Request, db_session, current_user_email, user_inputs):
    # load current user calcs
    list_current_user_calcs, list_current_user_calc_ids = current_user_calcs_and_ids(current_user_email, db_session)  # now ordered

    # # load calcs shared by current user
    # current_user_shared_with_emails, current_user_shared_calc_access_levels, current_user_shared_calc_details = (
    #     current_user_shared_calcs(current_user_email, db_session)
    # )

    ### forsøg
    current_user_shared_with_emails, current_user_shared_calc_access_levels, current_user_shared_calc_details = (
        current_user_shared_calcs(list_current_user_calc_ids, db_session)  # ordered calcs
    )
    ###


    print('logged_in_redirect:')
    print('current_user_shared_with_emails: ', current_user_shared_with_emails)
    print('current_user_shared_calc_access_levels: ', current_user_shared_calc_access_levels)



    # load calcs shared with current user
    all_shared_calcs_with_user, list_all_shared_calcs_access_level = (
        calcs_shared_with_current_user(current_user_email, db_session)
    )
    print('\nshared with current user:')
    print('all_shared_calcs_with_user: ', all_shared_calcs_with_user)
    print('list_all_shared_calcs_access_level: ', list_all_shared_calcs_access_level)

    principal = calculated_principal(user_inputs)

    context = {'request': request,
               'dropdown_bank_names': dropdown_bank_names,
               'input_house_price': principal.user_inputs['house_price'],
               'input_down_payment': principal.user_inputs['down_payment'],
               'input_bond_price': principal.user_inputs['bond_price'],
               'selected_bank': principal.user_inputs['dropdown'],
               'principal_value': principal.principal,
               'capital_loss': principal.capital_loss,
               'list_current_user_calcs': list_current_user_calcs,
               'all_shared_calcs_with_user': all_shared_calcs_with_user,
               'list_all_shared_calcs_access_level': list_all_shared_calcs_access_level,
               'current_user_shared_calc_details': current_user_shared_calc_details,
               'current_user_shared_calc_access_levels': current_user_shared_calc_access_levels,
               'current_user_shared_with_emails': current_user_shared_with_emails,
               }
    return views.TemplateResponse('logged_in.html', context)


def current_user_calcs_and_ids(current_user_email, db_session):
    current_user_id = get_current_user_id(current_user_email, db_session)

    ### forsøg med order by
    # Order by user_id and then by calc_id within each user_id
    list_current_user_calcs = (db_session.query(Calcs).filter(Calcs.user_id == current_user_id)
                               .order_by(asc(Calcs.user_id), asc(Calcs.calc_id))
                               .all())

    ###


    # list_current_user_calcs = db_session.query(Calcs).filter(Calcs.user_id == current_user_id).all()
    list_current_user_calc_ids = [calc.calc_id for calc in list_current_user_calcs]
    return list_current_user_calcs, list_current_user_calc_ids


def get_current_user_id(current_user_email, db_session):
    return db_session.query(Users.user_id).filter(Users.email == current_user_email).one()[0]


# def current_user_shared_calcs(current_user_email, db_session):
#
#     list_current_user_calcs, list_current_user_calc_ids = current_user_calcs_and_ids(current_user_email, db_session)  # TODO kan tage calc id som input i stedet for at kalde fkt igen her
#
#     # load calc info of calcs shared with few
#     list_sharedWithFew_emails, list_sharedWithFew_access_level, list_sharedWithFew_calc_details = (
#         get_calcs_sharedWithFew(list_current_user_calc_ids, db_session)
#     )
#
#     # load calc info of calcs shared with all
#     list_sharedWithAll_access_level, list_sharedWithAll_calc_details = (
#         get_calcs_sharedWithAll(list_current_user_calc_ids, db_session)
#     )
#
#     # combine calc info of all current user shared calcs
#     shared_with_emails = list_sharedWithFew_emails + ['alle brugere'] * len(list_sharedWithAll_access_level)
#     shared_with_access_levels = list_sharedWithFew_access_level + list_sharedWithAll_access_level
#     shared_with_calc_details = list_sharedWithFew_calc_details + list_sharedWithAll_calc_details
#
#     return shared_with_emails, shared_with_access_levels, shared_with_calc_details
# forsøg
def current_user_shared_calcs(list_current_user_calc_ids, db_session):  # ordered calcs

    # load calc info of calcs shared with few
    list_sharedWithFew_emails, list_sharedWithFew_access_level, list_sharedWithFew_calc_details = (
        get_calcs_sharedWithFew(list_current_user_calc_ids, db_session)
    )

    # load calc info of calcs shared with all
    list_sharedWithAll_access_level, list_sharedWithAll_calc_details = (
        get_calcs_sharedWithAll(list_current_user_calc_ids, db_session)
    )

    # combine calc info of all current user shared calcs
    shared_with_emails = list_sharedWithFew_emails + ['alle brugere'] * len(list_sharedWithAll_access_level)
    shared_with_access_levels = list_sharedWithFew_access_level + list_sharedWithAll_access_level
    shared_with_calc_details = list_sharedWithFew_calc_details + list_sharedWithAll_calc_details

    return shared_with_emails, shared_with_access_levels, shared_with_calc_details



def get_calcs_sharedWithFew(list_current_user_calc_ids, db_session):

    ### forsøg

    list_current_user_calcs_sharedWithFew = (db_session.query(SharedCalcsWithFew)
                                             .filter(SharedCalcsWithFew.calc_id.in_(list_current_user_calc_ids))
                                             .order_by(asc(SharedCalcsWithFew.user_id), asc(SharedCalcsWithFew.calc_id))
                                             .all()
                                             )  # ordered
    ###


    # load calcs shared with few others
    # list_current_user_calcs_sharedWithFew = (db_session.query(SharedCalcsWithFew)
    #                                          .filter(SharedCalcsWithFew.calc_id.in_(list_current_user_calc_ids))
    #                                          .all()
    #                                          )

    # get info about calcs shared with few others
    if not list_current_user_calcs_sharedWithFew:
        list_sharedWithFew_emails = []
        list_sharedWithFew_access_level = []
        list_sharedWithFew_calc_details = []
    else:

        list_sharedWithFew_user_ids = [calc.user_id for calc in list_current_user_calcs_sharedWithFew]

        ### forsøg
        list_sharedWithFew_emails = [crypto.decrypt(email) for _, email in
                                     db_session.query(SharedCalcsWithFew.user_id, Users.email)
                                     .join(Users, SharedCalcsWithFew.user_id == Users.user_id)
                                     .filter(SharedCalcsWithFew.user_id.in_(list_sharedWithFew_user_ids))
                                     .order_by(asc(SharedCalcsWithFew.user_id), asc(SharedCalcsWithFew.calc_id))
                                     .all()
                                     ]  # ordered
        ###



        # list_sharedWithFew_emails = [crypto.decrypt(email) for _, email in
        #                              db_session.query(SharedCalcsWithFew.user_id, Users.email)
        #                              .join(Users, SharedCalcsWithFew.user_id == Users.user_id)
        #                              .filter(SharedCalcsWithFew.user_id.in_(list_sharedWithFew_user_ids))
        #                              .all()
        #                              ]
        list_sharedWithFew_access_level = [calc.access_level for calc in list_current_user_calcs_sharedWithFew]

        # get calc details of the users shared calcs
        list_sharedWithFew_calc_ids = [calc.calc_id for calc in list_current_user_calcs_sharedWithFew]
        list_sharedWithFew_calc_details = [db_session.query(Calcs).filter(Calcs.calc_id == calc_id).one()
                                           for calc_id in list_sharedWithFew_calc_ids
                                           ]

    return list_sharedWithFew_emails, list_sharedWithFew_access_level, list_sharedWithFew_calc_details


def get_calcs_sharedWithAll(list_current_user_calc_ids, db_session):
    list_current_user_calcs_sharedWithAll = (db_session.query(SharedCalcsWithAll)
                                             .filter(SharedCalcsWithAll.calc_id.in_(list_current_user_calc_ids))
                                             .all()
                                             )

    if not list_current_user_calcs_sharedWithAll:
        list_sharedWithAll_access_level = []
        list_sharedWithAll_calc_details = []
    else:
        list_sharedWithAll_access_level = [calc.access_level for calc in list_current_user_calcs_sharedWithAll]
        list_sharedWithAll_calc_ids = [calc.calc_id for calc in list_current_user_calcs_sharedWithAll]
        list_sharedWithAll_calc_details = (db_session.query(Calcs)
                                           .filter(Calcs.calc_id.in_(list_sharedWithAll_calc_ids))
                                           .all()
                                           )
    return list_sharedWithAll_access_level, list_sharedWithAll_calc_details


def calcs_shared_with_current_user(current_user_email, db_session):
    current_user_id = get_current_user_id(current_user_email, db_session)

    # shared_with_all = db_session.query(SharedCalcsWithAll).filter(SharedCalcsWithAll.user_id == current_user_id).all()
    # shared_with_user = db_session.query(SharedCalcsWithFew).filter(SharedCalcsWithFew.user_id == current_user_id).all()

    ### forsøg
    shared_with_all = (db_session.query(SharedCalcsWithAll).filter(SharedCalcsWithAll.user_id == current_user_id)
                       .order_by(asc(SharedCalcsWithAll.user_id), asc(SharedCalcsWithAll.calc_id))
                       .all()
                       )  # ordered

    shared_with_user = (db_session.query(SharedCalcsWithFew).filter(SharedCalcsWithFew.user_id == current_user_id)
                        .order_by(asc(SharedCalcsWithFew.user_id), asc(SharedCalcsWithFew.calc_id))
                        .all()
                        )  # ordered
    ###


    all_shared_calcs_info = shared_with_all + shared_with_user
    all_shared_calc_ids = [shared_info.calc_id for shared_info in all_shared_calcs_info]

    ### forsøg
    all_shared_calcs_with_user = (db_session.query(Calcs).filter(Calcs.calc_id.in_(all_shared_calc_ids))
                                  .order_by(asc(Calcs.user_id), asc(Calcs.calc_id))
                                  .all()
                                  )
    ###

    # all_shared_calcs_with_user = db_session.query(Calcs).filter(Calcs.calc_id.in_(all_shared_calc_ids)).all()
    list_shared_access_level = [shared_info.access_level.value for shared_info in all_shared_calcs_info]
    return all_shared_calcs_with_user, list_shared_access_level


def calculated_principal(user_inputs: Dict):
    # first login where no inputs are specified or redirect where inputs needed for principal not specified
    if not user_inputs or 'house_price' not in user_inputs.keys():
        constructed_user_inputs = {'house_price': '1000000',
                                   'down_payment': '50000',
                                   'bond_price': '98,5',
                                   'dropdown': 'Totalkredit'
                                   }
        principal.calculate(constructed_user_inputs)

    else:
        principal.calculate(user_inputs)

    return principal


def calc_values(db_session, user_inputs):
    calc_values = db_session.query(Calcs).filter(Calcs.calc_id == user_inputs['calc_id']).one()
    calc_values_as_dict = {c.name: getattr(calc_values, c.name) for c in calc_values.__table__.columns}
    calc_values_as_dict['dropdown'] = calc_values_as_dict.pop('bank_name')
    return calc_values_as_dict


def user_if_exist(db_session, current_user_email):
    existing_users = db_session.query(Users).all()

    for existing_user in existing_users:
        user_exist = crypto.decrypt(existing_user.email) == current_user_email
        if user_exist:
            return existing_user
