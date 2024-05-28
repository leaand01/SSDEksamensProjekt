from dataclasses import dataclass, field

from Interfaces.ICalculator import ICalculator
from Interfaces.IProcessor import IProcessor
from Interfaces.IRepository import IRepository

from Services.PrincipalCalculator_helper_funcs import *


@dataclass
class ProcessUserInputs(IProcessor):

    def process(self, data: Dict[str, Union[str, float]]) -> Dict[str, Union[str, float]]:
        """Convert dict values of types int and float to numerics."""
        processed_data = data.copy()
        processed_data = keep_keys(processed_data)  # TODO: added
        key_value_pairs = processed_data.items()
        for key, value in key_value_pairs:
            if key == 'dropdown':
                continue

            value = convert_str_to_numeric(value)
            check_not_negative(value)

            if key in ['house_price', 'down_payment']:
                value = round(value)

            if key == 'bond_price':
                check_is_greater_than_two(value)
                value = convert_to_percentage(value)

            processed_data[key] = value

        return processed_data

    def transform_data_to_view_format(self, data: Dict[str, Union[str, float, int]]) -> Dict[str, Union[str, str]]:
        view_data = data.copy()

        key_value_pairs = view_data.items()
        for key, value in key_value_pairs:
            if key == 'dropdown':
                continue

            if key == 'bond_price':
                view_data[key] = convert_back_to_input_percentage_string(value)
                continue

            view_data[key] = convert_numeric_to_string_dk_punctuation(value)

        return view_data

    def transform_value_to_view_format(self, value: Union[float, int]) -> str:
        return convert_numeric_to_string_dk_punctuation(int(round(value)))


@dataclass
class Principal(ICalculator):
    """Calculater for calculating principal and capital loss."""
    banks: IRepository
    processor: IProcessor

    # defined when calling calculate
    user_inputs: Dict[str, Union[str, float]] = field(init=False, default_factory=dict)
    principal: int = field(init=False, default=None)
    capital_loss: int = field(init=False, default=None)

    def calculate(self, user_inputs: Dict[str, Union[str, float]]) -> str:
        self.user_inputs = self.processor.process(user_inputs)

        bank_name = self.user_inputs['dropdown']
        bank_details = self.banks.get(bank_name)

        loan_amount = self.user_inputs['house_price'] + bank_details.fees - self.user_inputs['down_payment']
        net_bond_price = self.user_inputs['bond_price'] - bank_details.bond_fee
        principal = loan_amount / net_bond_price
        capital_loss = principal - loan_amount

        self.user_inputs = self.processor.transform_data_to_view_format(self.user_inputs)
        self.principal = self.processor.transform_value_to_view_format(principal)
        self.capital_loss = self.processor.transform_value_to_view_format(capital_loss)

        return principal
