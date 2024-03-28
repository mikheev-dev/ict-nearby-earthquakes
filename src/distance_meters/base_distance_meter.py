from abc import ABC, abstractmethod

from src.point import Point


class BaseDistanceMeter(ABC):
    """
    Base class for calculating distance between two points.
    """
    @staticmethod
    @abstractmethod
    def dist(first: Point, second: Point) -> float:
        raise NotImplemented()

