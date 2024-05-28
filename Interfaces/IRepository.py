from abc import ABC, abstractmethod
from typing import TypeVar


T_input = TypeVar('T_input')
T_output = TypeVar('T_output')
T_output_all = TypeVar('T_output_all')


class IRepository(ABC):
    """Generic interface for accessing data."""

    @abstractmethod
    def get_all(self) -> T_output_all:
        """Return all data."""

    @abstractmethod
    def get(self, identifier: T_input) -> T_output:
        """Return name's data."""
