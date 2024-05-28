from abc import ABC, abstractmethod
from typing import TypeVar


T_input = TypeVar('T_input')
T_output = TypeVar('T_output')


class ICalculator(ABC):
    """Generic interface for calculator method."""

    @abstractmethod
    def calculate(self, data: T_input) -> T_output:
        """Calculate something."""
