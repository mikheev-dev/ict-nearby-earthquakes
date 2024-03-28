from typing import Type, List, Tuple

from src.point import Point
from src.earthquake import EarthQuake
from src.earthquakes_info_connectors import BaseEarthquakesInfoConnector, UsgsGovEarthquakesInfoConnector
from src.distance_meters import BaseDistanceMeter, HaversineDistanceMeter
from src.utils.squeezing_strategies import BaseSqueezingStrategy


class PointAnalyzer:
    """
        Class to analyze the closest earthquakes to given point.
    """
    __earthquakes_info_conn: Type[BaseEarthquakesInfoConnector]

    __point: Point

    def __init__(
            self,
            point: Point,
            eqs_info_con: Type[BaseEarthquakesInfoConnector] = UsgsGovEarthquakesInfoConnector,
    ):
        """
        :param point: Point on the Earth surface
        :param eqs_info_con: Connector to a source with info about earthquakes.
        """
        self.__point = point
        self.__earthquakes_info_conn = eqs_info_con

    @property
    def point(self) -> Point:
        return self.__point

    def find_closest_earthquakes(
            self,
            number_to_show: int | None = None,
            distance_meter: Type[BaseDistanceMeter] = HaversineDistanceMeter,
            squeezing_strategy: BaseSqueezingStrategy | None = None,
    ) -> List[Tuple[float, EarthQuake]]:
        """
        :param number_to_show: how many closest earthquakes should return, None means show everything
        :param distance_meter: class calculating the distance between two points on the Earth surface
        :param squeezing_strategy: should apply some strategy of grouping for instances for same values.
        :return:
        """
        eqs = self.__earthquakes_info_conn.get_earthquakes()
        if squeezing_strategy:
            eqs = squeezing_strategy.squeeze(
                list_to_squeeze=eqs,
            )
        distances_to_eqs = [
            (
                distance_meter.dist(self.__point, eq.point),
                eq
            )
            for eq in eqs
        ]
        distances_to_eqs.sort(
            key=lambda x: x[0]
        )
        return distances_to_eqs[:number_to_show]
