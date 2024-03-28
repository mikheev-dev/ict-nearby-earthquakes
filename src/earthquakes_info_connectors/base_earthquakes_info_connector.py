from abc import ABC, abstractmethod
from typing import List

from src.earthquake import EarthQuake


class BaseEarthquakesInfoConnector(ABC):
    """
        Base class for connectors to sources with information about earthquakes.
    """
    @classmethod
    @abstractmethod
    def get_earthquakes(cls) -> List[EarthQuake]:
        raise NotImplementedError
