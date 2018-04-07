import logging
from InputHandler import InputHandler
from CandidateGenerator import CandidateGenerator
import StationData

def run(trip_path="trips/cities-1.json"):
    input_handler = InputHandler()
    input_handler.read_input_file(trip_path)
    candidate_generator = CandidateGenerator(input_handler.requested_cities,
                                             input_handler.trip_days,
                                             input_handler.avg_city_stay)

    sd = StationData.StationData()

    trip_candidates = candidate_generator.get_n_most_popular_candidates(3)

    print([t.calculate_trip_distance(input_handler.requested_cities, sd.distance_between_stations) for t in trip_candidates])


    #if station_a is not None and station_b is not None:
    #    duration = StationData.time_between_stations(station_a, station_b)
    #    logging.debug("It takes approximately {0} hours to travel from {1} to {2}".format(duration,
     #                                                                                     station_a["name"],
     #                                                                                     station_b["name"]))


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s')

    run()
