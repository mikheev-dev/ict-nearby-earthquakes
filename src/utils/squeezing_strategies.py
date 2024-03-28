from abc import ABC, abstractmethod
from collections import defaultdict
from typing import List, Dict


class BaseSqueezingStrategy(ABC):
    """
    Base class for squeezing lists, if we need to group somehow instances with same field.
    It requires _field_to_squeeze_on to be a attribute of instances inside the list.
    """
    _field_to_squeeze_on: str

    def __init__(self, field_to_squeeze_on: str):
        self._field_to_squeeze_on = field_to_squeeze_on

    @abstractmethod
    def squeeze(
            self,
            list_to_squeeze: List,
    ) -> List:
        raise NotImplementedError


class OnlyOneSqueezingStrategy(BaseSqueezingStrategy):
    """
        Class for squeezing lists with the strategy:
        save only one element of all instances with same value of _field_to_squeeze_on
    """
    def squeeze(
            self,
            list_to_squeeze: List,
    ) -> List:
        try:
            grouped_list_by_field: Dict = defaultdict(list)
            for el in list_to_squeeze:
                field_value = getattr(el, self._field_to_squeeze_on)
                grouped_list_by_field[field_value].append(el)
            return [
                group[0]
                for group in grouped_list_by_field.values()
            ]
        except AttributeError:
            raise Exception(f"Can't squeeze list, no field {self._field_to_squeeze_on} of instances inside the list.")
