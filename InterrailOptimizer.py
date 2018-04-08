import logging
from InputHandler import InputHandler
from CandidateGenerator import CandidateGenerator
from CandidateRanker import get_top_n_trips
import StationData


def run(trip_path="trips/cities-1.json"):
    input_handler = InputHandler()
    input_handler.read_input_file(trip_path)
    candidate_generator = CandidateGenerator(input_handler.requested_cities,
                                             input_handler.trip_days,
                                             input_handler.avg_city_stay)

    trip_candidates = candidate_generator.get_n_most_popular_candidates(10)

    for trip in trip_candidates:
        trip.calculate_trip_distances(input_handler.requested_cities,
                                      input_handler.starting_station,
                                      StationData.StationData.time_between_stations)
        trip.find_optimal_route()
        trip.calculate_route_score(input_handler.requested_cities, input_handler.all_travellers)

    winning_trips = get_top_n_trips(trip_candidates, 5)

    print("\n".join([str(t) for t in winning_trips]))


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s')

    run()
