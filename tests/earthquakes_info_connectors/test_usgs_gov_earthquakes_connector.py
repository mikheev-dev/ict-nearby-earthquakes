import geojson
import os
import pytest
import requests

from src.earthquakes_info_connectors import UsgsGovEarthquakesInfoConnector, UsgsGovEarthquakeParser

from tests.utils_for_tests import gen_earthquakes_info


class TestUsgsGovEarthquakesInfoConnector:
    URL_PATH = os.path.join(
        UsgsGovEarthquakesInfoConnector.EARTHQUAKE_SERVICE_URL,
        UsgsGovEarthquakesInfoConnector.EARTHQUAKES_30_DAYS_PATH,
    )

    @pytest.mark.parametrize('status_code', [201, 300, 301, 400, 404, 500])
    def test_bad_connection(self, requests_mock, status_code):
        requests_mock.get(self.URL_PATH, text='error', status_code=status_code)
        with pytest.raises(
                Exception,
                match="Can't fetch info about earthquakes for last 30 days."
        ):
            UsgsGovEarthquakesInfoConnector.get_earthquakes()


class TestUsgsGovEarthquakeParser:
    __parser = UsgsGovEarthquakeParser

    def test_no_metadata(self):
        data = {"foo": "bar"}
        with pytest.raises(
            Exception,
            match=f"Can't parse the response {data}"
        ):
            self.__parser.parse(geojson.dumps(data))

    def test_no_status_in_metadata(self):
        data = {"metadata": {"foo": "bar"}}
        with pytest.raises(
            KeyError
        ):
            self.__parser.parse(geojson.dumps(data))

    @pytest.mark.parametrize('status_code', [201, 300, 301, 400, 404, 500])
    def test_bad_status_in_metadata(self, status_code):
        data = {"metadata": {"status": status_code, "url": "test.com"}}
        with pytest.raises(
            Exception,
            match="Can't parse the response from test.com, invalid status code"
        ):
            self.__parser.parse(geojson.dumps(data))

    def test_no_features_in_response(self):
        data = {"metadata": {"status": 200, "url": "test.com"}}
        with pytest.raises(
            Exception,
            match="No features got in response"
        ):
            self.__parser.parse(geojson.dumps(data))

    def test_empty_response_list(self):
        data = {"metadata": {"status": 200, "url": "test.com"}, "features": []}
        eqs = self.__parser.parse(geojson.dumps(data))
        assert len(eqs) == 0

    def test_incorrect_features(self):
        data = {"metadata": {"status": 200, "url": "test.com"}, "features": [{"foo": "bar"}]}
        with pytest.raises(
                KeyError,
        ):
            self.__parser.parse(geojson.dumps(data))

    def test_correct_case(self):
        generated_eqs = gen_earthquakes_info()
        data = {
            "metadata": {"status": 200, "url": "test.com"},
            "features": [
                {
                    "id": eq.id,
                    "geometry": {
                        "coordinates": [eq.point.lon, eq.point.lat, 0.]
                    },
                    "properties": {
                        "mag": eq.mag,
                        "place": eq.place,
                        "title": eq.title,
                    },
                }
                for eq in generated_eqs
            ]
        }
        parsed_eqs = self.__parser.parse(geojson.dumps(data))

        assert len(parsed_eqs) == len(generated_eqs)
        assert parsed_eqs == generated_eqs
