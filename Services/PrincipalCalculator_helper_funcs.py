import locale
import string
from typing import Union, Dict


def keep_keys(user_inputs: Dict):
    keys_to_keep = ['house_price', 'down_payment', 'bond_price', 'dropdown']

    filtered_dict = {key: value for key, value in user_inputs.items() if key in keys_to_keep}
    return filtered_dict


def convert_str_to_numeric(value: str) -> float:
    """Can only convert if punctuation follows danish conventions."""
    check_not_empty(value)
    check_no_invalid_punctuations(value)
    check_no_letters(value)
    value = as_numeric_using_dk_punctuation(value)
    return value


def check_not_empty(value: str) -> None:
    if not value.replace(' ', ''):
        raise ValueError('Empty input!')


def check_no_invalid_punctuations(value: str) -> None:
    invalid_punctuations = string.punctuation.replace(',', '').replace('.', '')
    if any([x in invalid_punctuations for x in value]):
        raise ValueError('Invalid input!')


def check_no_letters(value: str) -> None:
    letters = string.ascii_lowercase
    if any([x in letters for x in value.lower()]):
        raise ValueError('The input must only contain digits!')


def as_numeric_using_dk_punctuation(value: str) -> Union[float, int]:
    """Convert string to float. String must only contain danish punctuations if any."""
    try:
        locale.setlocale(locale.LC_ALL, 'da_DK.UTF-8')
        return locale.atof(value)
    except ValueError:
        raise ValueError('Incorrect number: Danish punctuation uses "," for decimal and "." for 1000 seperator.')


def check_not_negative(value: float) -> None:
    if isinstance(value, float) and value < 0:
        raise ValueError('Inputted number must be >= 0!')


def check_is_greater_than_two(value: float) -> None:
    if value <= 2:
        raise ValueError('Bond price must be greater than 2, due to bank bond fees.!')


def convert_to_percentage(value: Union[float, int]) -> float:
    return value / 100


def convert_back_to_input_percentage_string(value: Union[float, int]) -> str:
    n_dec = min(n_decimals(value) - 2, 3)
    n_dec = max(n_dec, 0)
    return '{:.{}%}'.format(value, n_dec).replace('.', ',').replace('%', '')


def n_decimals(value: Union[int, float]) -> int:
    try:
        n_dec = len(str(value).split('.')[1])
    except IndexError:
        n_dec = 0
    return n_dec


def convert_numeric_to_string_dk_punctuation(value: Union[float, int]) -> str:
    return '{:,}'.format(value).replace(',', '.')
