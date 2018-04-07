from itertools import permutations
import StationData


class Trip:

    def __init__(self, city_names, votes, votees):
        self.city_names = city_names
        self.votes = votes
        self.votees = votees
        self.distances = {}

    def calculate_trip_distance(self, requested_cities, distance_method):
        for city_a, city_b in list(permutations(self.city_names, 2)):
            distance = distance_method(requested_cities[city_a], requested_cities[city_a])
            print(distance)
            self.distances[city_a][city_b] = distance

        return self.distances

