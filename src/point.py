from dataclasses import dataclass
from typing import Tuple


@dataclass
class Point:
    """
    Class to describe Point on the Earth surface with lan and lon.
    """
    lon: float
    lat: float
