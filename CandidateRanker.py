

def get_top_n_trips(optimized_trip_candidates, n):
    if len(optimized_trip_candidates) <= n:
        return optimized_trip_candidates

    sorted_candidates = sorted(optimized_trip_candidates, key=lambda trip: trip.score, reverse=True)
    return sorted_candidates[:n]