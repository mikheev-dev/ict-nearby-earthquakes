from typing import List

from src.distance_meters import BaseDistanceMeter
from src.earthquakes_info_connectors import BaseEarthquakesInfoConnector
from src.point import Point
from src.earthquake import EarthQuake


class DistanceMeterForTest(BaseDistanceMeter):
    @staticmethod
    def dist(first: Point, second: Point) -> float:
        return abs(first.lon - second.lon) + abs(first.lat - second.lat)


EARTHQUAKE_INFO_SIZE = 10


def gen_earthquakes_info() -> List[EarthQuake]:
    return [
        EarthQuake(**{
            "point": Point(
                lat=10. * (EARTHQUAKE_INFO_SIZE - idx),
                lon=2. * (EARTHQUAKE_INFO_SIZE - idx),
            ),
            "id": f"eq{idx}",
            "place": f"place{idx}",
            "title": f"eq at place {idx}",
            "mag": 1.5 * idx
        })
        for idx in range(EARTHQUAKE_INFO_SIZE)
    ]

