def compute_wait_time(street_to_arrival_times_map: dict, schedule: list, max_sim_time: int) -> int:
    """
    Computes the total waiting time of all cars at this intersection.

    :param street_to_arrival_times_map: A dictionary that maps from street name (str) to list of arrival times (int)
    :return: total wait time (int)
    """
    # max_arrival_time = -1
    #
    # for street_name, arrival_times in street_to_arrival_times_map.items():
    #     max_arrival_time = max(arrival_times[-1], max_arrival_time)

    # go through schedule
    street_to_num_waiting_cars_map = {}
    street_to_pointers_arrival_times = {}
    for t in range(max_sim_time):
        if street_to_num_waiting_cars_map[]

if __name__ == '__main__':
    street_to_arrival_times_map = {
        'rue-paris': [0, 1, 4, 10],
        'rue-barcelone': [5, 6]
    }

    schedule = [('rue-paris', 2), ('rue-barcelone', 1)]

    max_sim_time = 15

    compute_wait_time(street_to_arrival_times_map, schedule, max_sim_time)