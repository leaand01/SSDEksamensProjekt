from abc import ABC, abstractmethod
from typing import TypeVar


T = TypeVar('T')


class IDB(ABC):
    """Generic interface for calling some database."""

    @abstractmethod
    def query(self) -> T:
        """Returns all data from database."""
