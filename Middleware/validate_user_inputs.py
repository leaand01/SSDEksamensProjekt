import re
from fastapi import HTTPException, status, Request

from Services.PrincipalCalculator_helper_funcs import check_not_empty, check_no_invalid_punctuations, check_no_letters


async def validate_user_inputs(request: Request, call_next):
    if request.method == "POST":
        form_data = await request.form()
        form_data = dict(form_data)

        # Cache the form data in the request state such that it is accessible in the endpoints
        request.state.form_data = form_data

        if 'house_price' in form_data:
            validate_numeric_string(form_data['house_price'])

        if 'down_payment' in form_data:
            validate_numeric_string(form_data['down_payment'])

        if 'bond_price' in form_data:
            validate_numeric_string(form_data['bond_price'])

        if 'share_with_single_user' in form_data:  # email inputted by user
            validate_first_character(form_data['share_with_single_user'])
            validate_gmail_address(form_data['share_with_single_user'])

    response = await call_next(request)
    return response


def validate_numeric_string(value: str) -> None:
    try:
        validate_first_character(value)
        check_not_empty(value)
        check_no_invalid_punctuations(value)
        check_no_letters(value)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad Request: Invalid parameters")


def validate_first_character(value: str) -> None:
    first_character = value.replace(' ', '')[0]
    if first_character in '.,':
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad Request: Invalid parameters")


def validate_gmail_address(email: str) -> None:
    gmail_regex = r'^[a-zA-Z0-9._%+-]+@gmail\.com$'

    if not re.match(gmail_regex, email):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Gmail address")
