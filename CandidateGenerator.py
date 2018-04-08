import logging
from itertools import combinations
from Trip import Trip


class CandidateGenerator:

    def __init__(self, requested_cities, trip_days, avg_city_stay):
        self.requested_cities = requested_cities
        self.total_cities = len(requested_cities)
        self.cities_per_trip_candidate = self._calculate_number_of_cities(trip_days, avg_city_stay)

        self._generate_all_combinations()

    def _generate_all_combinations(self):
        logging.info("Generating trip candidates with {0} cities each".format(self.cities_per_trip_candidate))

        if self.total_cities < self.cities_per_trip_candidate:
            only_trip = self.requested_cities.keys()
            trip_votes = self._get_trip_total_votes(only_trip)
            trip_votees = self._get_trip_total_votees(only_trip)
            self.all_combinations = [Trip(only_trip, trip_votes, trip_votees)]

        candidate_list = list(combinations(self.requested_cities.keys(), self.cities_per_trip_candidate))
        self.all_combinations = [Trip(trip_cities, self._get_trip_total_votes(trip_cities), self._get_trip_total_votees(trip_cities)) for trip_cities in candidate_list]

    def get_n_most_popular_candidates(self, n):
        if len(self.all_combinations) <= n:
            return self.all_combinations

        top_n = sorted(self.all_combinations, key=lambda trip: trip.votes)[-n:]
        return top_n

    def _get_trip_total_votes(self, trip_cities):
        vote_sum = 0
        for city in trip_cities:
            vote_sum += self._get_city_votes(city)
        return vote_sum

    def _get_trip_total_votees(self, trip_cities):
        votees = []
        for city in trip_cities:
            votees += self._get_city_votees(city)
        return list(set(votees))

    def _get_city_votes(self, station_name):
        return self.requested_cities[station_name]["votes"]

    def _get_city_votees(self, station_name):
        return self.requested_cities[station_name]["votees"]

    @staticmethod
    def _calculate_number_of_cities(trip_days, avg_city_stay):
        return round(trip_days / avg_city_stay)