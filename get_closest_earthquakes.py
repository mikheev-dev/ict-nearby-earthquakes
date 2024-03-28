from typing import List, Tuple

import logging

from src.distance_meters import HaversineDistanceMeter
from src.earthquake import EarthQuake
from src.earthquakes_info_connectors import UsgsGovEarthquakesInfoConnector
from src.point import Point
from src.point_analyzer import PointAnalyzer
from src.utils.squeezing_strategies import OnlyOneSqueezingStrategy


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def read_input_point() -> Point:
    print("Enter coordinates for the point of interest:")
    latitude = float(input())
    longitude = float(input())
    return Point(
        lat=latitude,
        lon=longitude,
    )


def output(earthquakes_and_distances: List[Tuple[float, EarthQuake]]):
    for dist, eq in earthquakes_and_distances:
        print(f"{eq.title} || {dist:.0f}")


if __name__ == "__main__":
    point = read_input_point()
    logging.debug(f"Got point {point} from input.")
    logging.debug(f"Computing closest earthquakes to point {point}.")

    closest_earthquakes_with_distances: List[Tuple[float, EarthQuake]] = PointAnalyzer(
        point=point,
        eqs_info_con=UsgsGovEarthquakesInfoConnector,
    ).find_closest_earthquakes(
        number_to_show=10,
        distance_meter=HaversineDistanceMeter,
        squeezing_strategy=OnlyOneSqueezingStrategy(
            field_to_squeeze_on='place',
        ),
    )

    logging.debug(f"Closest earthquakes to point {point}:\n{closest_earthquakes_with_distances}")
    output(closest_earthquakes_with_distances)
