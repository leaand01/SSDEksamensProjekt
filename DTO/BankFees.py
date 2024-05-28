from dataclasses import dataclass


@dataclass
class BankFees:
    name: str
    fees: float
    bond_fee: float
