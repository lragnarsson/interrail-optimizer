import logging
import pandas as pd
import gpxpy.geo
from geopy.geocoders import Nominatim


class StationData:

    def __init__(self, railway_data_path="data/european-train-stations.csv"):
        self.all_station_data = pd.read_csv(railway_data_path, sep=";", usecols=self.interesting_columns)
        self.logger = logging.getLogger("StationData")

    @staticmethod
    def _station_row_to_dict(row):
        station_dict = row.to_dict("records")[0]
        # Convert lat/lon string into two float fields:
        lat, lon = station_dict["latlong"].split(", ")
        station_dict["lat"] = float(lat)
        station_dict["lon"] = float(lon)
        del station_dict["latlong"]

        return station_dict

    # Helper functino to try getting a main station or city station if we have multiple rows
    @staticmethod
    def _create_dict_if_unique(matching_rows):
        if len(matching_rows) == 1:
            return StationData._station_row_to_dict(matching_rows)
        if len(matching_rows) > 1:  # More than one result, try to find a unique one:
            uic_station_rows = matching_rows[~matching_rows["uic"].isnull()]
            if len(uic_station_rows) == 1:
                return StationData._station_row_to_dict(uic_station_rows)

            # See if there is a main station:
            main_station_rows = matching_rows[matching_rows["is_main_station"] == "t"]
            if len(main_station_rows) == 1:
                return StationData._station_row_to_dict(main_station_rows)
            if len(main_station_rows) > 1:  # More than one main station, see if there is one city station
                city_station_rows = main_station_rows[main_station_rows["is_city"] == "t"]
                if len(city_station_rows) == 1:
                    return StationData._station_row_to_dict(city_station_rows)

        return None

    def _get_station_from_name(self, city_name, country_code):
        self.logger.debug("Looking for station in {0} {1}".format(city_name, country_code))

        in_country = (self.all_station_data["country"].str.contains(country_code))
        # Try to find exact match:
        exact_match = self.all_station_data[
            (self.all_station_data["name"] == city_name) & in_country]
        station = self._create_dict_if_unique(exact_match)

        if station is not None:
            self.logger.debug("Station {0} was found".format(station["name"]))
            return station

        # Try to find partial match (e.g. find 'Stockholm Central' by searching for 'Stockholm')
        matching_rows = self.all_station_data[
            (self.all_station_data["name"].str.contains(city_name)) & in_country]
        station = self._create_dict_if_unique(matching_rows)

        if station is None:
            matching_names = matching_rows["name"].values
            if len(matching_names) == 0:
                self.logger.debug("Could not find any station in {0}".format(city_name))
            else:
                self.logger.debug("Could not find unique station, matches:\n-----\n{0}".format("\n".join(matching_names)))
            return station

        self.logger.debug("Station {0} was found".format(station["name"]))
        return station

    def _get_station_from_translated_name(self, city_name, country_code):
        in_country = (self.all_station_data["country"].str.contains(country_code))
        geolocator = Nominatim()
        location_data = geolocator.geocode({"city": city_name, "country": country_code})

        station = None
        if location_data is not None:
            local_name = location_data.address.split(",")[0].title()
            self.logger.debug("Looking for station in {0} {1}".format(local_name, country_code))
            # Try finding exact match of translated name:
            exact_matching_local_rows = self.all_station_data[
                (self.all_station_data["name"] == local_name) & in_country]
            station = self._create_dict_if_unique(exact_matching_local_rows)
            if station is not None:
                self.logger.debug("Station {0} was found".format(station["name"]))
                return station

            # Try finding partial match of translated name:
            matching_local_rows = self.all_station_data[
                (self.all_station_data["name"].str.contains(local_name)) & in_country]
            station = self._create_dict_if_unique(matching_local_rows)

            # We found nothing, or multiple matches.
            if station is None:
                matching_names = matching_local_rows["name"].values
                self.logger.debug("Could not find unique station from translated name, matches:\n-----\n{0}".format("\n".join(matching_names)))
                return None

        self.logger.debug("Station {0} was found".format(station["name"]))
        return station

    def get_station_dict(self, city_name, country_code=""):
        city_name = city_name.title()
        country_code=country_code.upper()

        station = self._get_station_from_name(city_name, country_code)
        if station is None: # Try translating city to local language if it wasn't found first times:
            station = self._get_station_from_translated_name(city_name, country_code)

        if station is None:
            self.logger.warning("No station was found in {0} {1}".format(city_name, country_code))
        return station

    # Calculates the straight line distance between two stations
    @staticmethod
    def distance_between_stations(station_a, station_b):
        return gpxpy.geo.haversine_distance(station_a["lat"], station_a["lon"],
                                            station_b["lat"], station_b["lon"])

    # Calculates an approximate time between two cities by train
    @staticmethod
    def time_between_stations(station_a, station_b, average_speed_kms=100):
        average_speed_ms = average_speed_kms / 3.6
        distance = StationData.distance_between_stations(station_a, station_b)
        time_s = distance / average_speed_ms
        return time_s / 3600

    # Constants:
    interesting_columns = [
        "id",
        "name",
        "latlong",
        "slug",
        "uic",
        "uic8_sncf",
        "parent_station_id",
        "is_city",
        "country",
        "is_main_station",
        "time_zone",
        "is_suggestable",
        "same_as"
    ]


