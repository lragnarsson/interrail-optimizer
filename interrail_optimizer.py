import logging
from StationData import StationData


def run():
    station_data = StationData()
    station_a = station_data.get_station_dict("linköping")
    station_b = station_data.get_station_dict("Krakow", "pl")

    if station_a is not None and station_b is not None:
        duration = StationData.time_between_stations(station_a, station_b)
        logging.debug("It takes approximately {0} hours to travel from {1} to {2}".format(duration,
                                                                                          station_a["name"],
                                                                                          station_b["name"]))


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s')

    run()
