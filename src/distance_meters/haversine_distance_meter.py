from haversine import haversine

from src.distance_meters.base_distance_meter import BaseDistanceMeter
from src.point import Point


class HaversineDistanceMeter(BaseDistanceMeter):
    """
        Class for calculating distance between two points on Earth with haversine formula.
    """
    @staticmethod
    def dist(first: Point, second: Point) -> float:
        return haversine(
            (first.lat, first.lon),
            (second.lat, second.lon),
        )
