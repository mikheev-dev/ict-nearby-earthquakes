from typing import List, Dict

import logging
import os
import requests
import geojson

from src.earthquakes_info_connectors.base_earthquakes_info_connector import BaseEarthquakesInfoConnector
from src.earthquake import EarthQuake
from src.point import Point

logger = logging.getLogger(__name__)


class UsgsGovEarthquakeParser:
    """
        Class to parse info about earthquakes for last 30 days from usgs.gov.
    """
    @staticmethod
    def extract_features(eq_data: Dict) -> List[Dict]:
        features = eq_data.get("features")
        if features is None:
            raise Exception("No features got in response")
        return features

    @staticmethod
    def check_response(eq_data: Dict):
        metadata = eq_data.get("metadata")
        if not metadata:
            raise Exception(f"Can't parse the response {eq_data}")
        if metadata["status"] != 200:
            url = metadata["url"]
            raise Exception(f"Can't parse the response from {url}, invalid status code")

    @classmethod
    def parse(cls, data: str) -> List[EarthQuake]:
        eq_data = geojson.loads(data)
        cls.check_response(eq_data)
        features = cls.extract_features(eq_data)
        eqs = []
        for f in features:
            coordinates = f["geometry"]["coordinates"]
            eqs.append(
                EarthQuake(
                    id=f["id"],
                    place=f["properties"]["place"],
                    mag=f["properties"]["mag"],
                    point=Point(
                        lon=coordinates[0],
                        lat=coordinates[1],
                    ),
                    title=f["properties"]["title"],
                )
            )
        return eqs


class UsgsGovEarthquakesInfoConnector(BaseEarthquakesInfoConnector):
    """
       Class to retrieve information about earthquakes from usgs.gov.
       Using handler to get information only for last month.
   """
    EARTHQUAKE_SERVICE_URL = "https://earthquake.usgs.gov/earthquakes/feed/v1.0"
    EARTHQUAKES_30_DAYS_PATH = "summary/all_month.geojson"

    @classmethod
    def get_earthquakes(cls) -> List[EarthQuake]:
        logging.debug("Get info about earthquakes.")
        eq_data = requests.get(
            url=os.path.join(
                cls.EARTHQUAKE_SERVICE_URL,
                cls.EARTHQUAKES_30_DAYS_PATH
            )
        )
        if eq_data.status_code != 200:
            raise Exception("Can't fetch info about earthquakes for last 30 days.")

        return UsgsGovEarthquakeParser.parse(eq_data.content.decode())

