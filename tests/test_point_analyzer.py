from unittest.mock import patch

import pytest

from src.utils import OnlyOneSqueezingStrategy
from src.earthquakes_info_connectors import UsgsGovEarthquakesInfoConnector
from src.point import Point
from src.point_analyzer import PointAnalyzer

from tests.utils_for_tests import (
    DistanceMeterForTest,
    gen_earthquakes_info,
    EARTHQUAKE_INFO_SIZE,
)


class TestPointAnalyzer:
    __point_analyzer: PointAnalyzer = PointAnalyzer(
        point=Point(lat=0.0, lon=0.0),
        eqs_info_con=UsgsGovEarthquakesInfoConnector,
    )

    @pytest.mark.parametrize('number_to_show', [0, 5, 8, EARTHQUAKE_INFO_SIZE, 100, None])
    def test_correct_case(self, number_to_show):
        info = gen_earthquakes_info()
        with patch.object(UsgsGovEarthquakesInfoConnector, 'get_earthquakes', return_value=info) as mock_method:
            eqs_with_distances = self.__point_analyzer.find_closest_earthquakes(
                number_to_show=number_to_show,
                distance_meter=DistanceMeterForTest,
                squeezing_strategy=None,
            )

        if number_to_show is None or number_to_show > len(info):
            number_to_show = len(info)

        assert len(eqs_with_distances) == number_to_show

        info = sorted(info, key=lambda eq: eq.point.lat + eq.point.lon)
        assert info[:number_to_show] == [eq for _, eq in eqs_with_distances]

    @pytest.mark.parametrize('number_to_show', [0, 5, 8, EARTHQUAKE_INFO_SIZE, 100, None])
    @pytest.mark.parametrize('squeezing_strategy', [None, OnlyOneSqueezingStrategy(field_to_squeeze_on='place')])
    def test_correct_case_with_squeezing_strategy_on_duplicated_info(self, number_to_show, squeezing_strategy):
        info = gen_earthquakes_info()
        with patch.object(
                UsgsGovEarthquakesInfoConnector,
                'get_earthquakes',
                return_value=info * 2
        ) as mock_method:
            eqs_with_distances = self.__point_analyzer.find_closest_earthquakes(
                number_to_show=number_to_show,
                distance_meter=DistanceMeterForTest,
                squeezing_strategy=squeezing_strategy,
            )

        eqs = [eq for _, eq in eqs_with_distances]
        info = sorted(info, key=lambda eq: eq.point.lat + eq.point.lon)

        if squeezing_strategy:
            if number_to_show is not None and number_to_show < len(info):
                assert len(eqs_with_distances) == number_to_show
                assert info[:number_to_show] == eqs
            else:
                assert info == eqs
        else:
            duplicated_info = sorted(info * 2, key=lambda eq: eq.point.lat + eq.point.lon)
            if number_to_show is None or number_to_show >= len(duplicated_info):
                assert duplicated_info == eqs
            else:
                assert eqs == duplicated_info[:number_to_show]

    @pytest.mark.parametrize('number_to_show', [0, 5, 8, EARTHQUAKE_INFO_SIZE, 100, None])
    @pytest.mark.parametrize('squeezing_strategy', [None, OnlyOneSqueezingStrategy(field_to_squeeze_on='place')])
    def test_empty_info(self,  number_to_show, squeezing_strategy):
        info = []
        with patch.object(
                UsgsGovEarthquakesInfoConnector,
                'get_earthquakes',
                return_value=info
        ) as mock_method:
            eqs_with_distances = self.__point_analyzer.find_closest_earthquakes(
                number_to_show=number_to_show,
                distance_meter=DistanceMeterForTest,
                squeezing_strategy=squeezing_strategy,
            )

        assert len(eqs_with_distances) == 0
