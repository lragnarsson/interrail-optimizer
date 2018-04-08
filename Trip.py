from itertools import permutations


class Trip:

    def __init__(self, city_names, votes, votees):
        self.city_names = city_names
        self.votes = votes
        self.votees = votees
        self.starting_city_name = ""
        self.distances = {}
        self.optimal_route = []
        self.total_train_time = 0
        self.longest_train_ride = 0
        self.score = 0

    def __str__(self):
        return str(self.optimal_route) + "  - score: " + str(self.score)

    def calculate_trip_distances(self, requested_cities, starting_city, distance_method):
        self.starting_city_name = starting_city["name"]
        all_cities = requested_cities.copy()
        all_cities[self.starting_city_name ] = starting_city
        for city_a, city_b in list(permutations(self.city_names + (self.starting_city_name,), 2)):
            distance = distance_method(all_cities[city_a], all_cities[city_b])
            self.distances[(city_a, city_b)] = distance

        return self.distances

    def find_optimal_route(self):
        best_route = [self.starting_city_name] + list(self.city_names)
        route_station_count = len(best_route)
        best_route_length = self._calculate_route_length(best_route)
        new_best = True

        while new_best:
            new_best = False
            for i in range(0, route_station_count):
                for j in range(i+1, route_station_count):
                    new_route = best_route.copy()
                    # Swap two stations around:
                    tmp = new_route[i]
                    new_route[i] = new_route[j]
                    new_route[j] = tmp
                    new_route_length = self._calculate_route_length(new_route)

                    if new_route_length < best_route_length:
                        best_route_length = new_route_length
                        best_route = new_route
                        new_best = True

        self.optimal_route = self._rotate_route_to_start(best_route, self.starting_city_name)
        self.total_train_time = best_route_length

    def calculate_route_score(self, requested_cities, all_travellers):
        time_score = self._calculate_time_score(requested_cities)
        vote_score = self._calculate_vote_score(requested_cities, all_travellers)
        self.score = time_score + vote_score

    def _calculate_time_score(self, requested_cities):
        return 200.0 / self.total_train_time

    def _calculate_vote_score(self, requested_cities, all_travellers):
        trip_destinations = self.optimal_route[1:]
        trip_votes = 0
        trip_votees = []

        for station in trip_destinations:
            station_data = requested_cities[station]
            trip_votes += station_data["votes"]
            trip_votees += station_data["votees"]

        votee_happiness_squared = []
        for traveller in all_travellers:
            votee_happiness_squared.append(pow(trip_votees.count(traveller), 2))

        mean_squared_happiness = sum(votee_happiness_squared) / float(len(votee_happiness_squared))
        min_happiness = min(votee_happiness_squared)

        return trip_votes + mean_squared_happiness * min_happiness

    def _calculate_route_length(self, route):
        total_length = 0
        cities_in_route = len(route)
        for idx in range(0, cities_in_route):
            station_pair = (route[idx],
                            route[(idx+1) % cities_in_route])
            total_length += self.distances[station_pair]

        return total_length

    @staticmethod
    def _rotate_route_to_start(route, starting_station):
        start_city_idx = route.index(starting_station)
        return route[start_city_idx:] + route[:start_city_idx]
