import json
import logging
from StationData import StationData


class InputHandler:

    def __init__(self, railway_data_path=None):
        self.station_data = StationData() if railway_data_path is None else StationData(railway_data_path)
        self.requested_cities = {}
        self.starting_station = None
        self.trip_days = 0
        self.avg_city_stay = 0

    def read_input_file(self, file_path):
        with open(file_path) as trip_file:
            input_data = json.load(trip_file)

            self.starting_station = self.station_data.get_station_dict(input_data["starting_city"])
            if self.starting_station is None:
                return

            self.trip_days = input_data["trip_days"]
            self.avg_city_stay = input_data["avg_city_stay"]
            self._load_traveller_requests(input_data["travellers"])

    def _load_traveller_requests(self, traveller_requests):
        for traveller in traveller_requests:
            traveller_name = traveller["name"]
            logging.debug("Loading cities for traveller: " + traveller_name)
            for city_string in traveller["cities"]:
                city_station = self.station_data.get_station_dict(city_string)
                if city_station is None:
                    return

                self._add_station_to_list(city_station, traveller_name)

    def _add_station_to_list(self, city_station, traveller_name):
        # Append city if new, otherwise add another vote to it:
        station_name = city_station["name"]
        if station_name in self.requested_cities.keys():
            self.requested_cities[station_name]["votes"] += 1
            self.requested_cities[station_name]["votees"].append(traveller_name)
        else:
            city_station["votes"] = 1
            city_station["votees"] = [traveller_name]
            self.requested_cities[station_name] = city_station

