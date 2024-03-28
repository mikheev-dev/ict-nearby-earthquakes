from dataclasses import dataclass

from src.point import Point


@dataclass
class EarthQuake:
    """
        Class for earthquake object.
        Could be extended in case of need to get additional information.
    """
    id: str
    point: Point
    mag: float
    place: str
    title: str | None = None
