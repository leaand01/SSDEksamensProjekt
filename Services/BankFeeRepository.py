from dataclasses import dataclass

from DTO.BankFees import BankFees
from Interfaces.IDB import IDB
from Interfaces.IRepository import IRepository


@dataclass
class LocalDB(IDB):
    """Access locally defined database."""
    local_db: dict[BankFees]

    def query(self) -> dict[BankFees]:
        return self.local_db


@dataclass
class Banks(IRepository):
    """Object for accessing bank details."""
    db: IDB

    def get_all(self) -> IDB:
        return self.db.query()

    def get(self, identifier: str) -> BankFees:
        return self.db.query()[identifier]
