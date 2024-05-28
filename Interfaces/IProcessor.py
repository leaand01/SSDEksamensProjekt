from abc import ABC, abstractmethod
from typing import TypeVar

T_input = TypeVar('T_input')
T_output = TypeVar('T_output')


class IProcessor(ABC):
    """Generic interface for processing some input"""

    @abstractmethod
    def process(self, data: T_input) -> T_output:
        """Do some processing"""
