import math


def compute_wait_time(street_to_arrival_times_map: dict, inters_schedule: list, max_sim_time: int) -> int:
    """
    Computes the total waiting time of all cars at this intersection.

    :param street_to_arrival_times_map: A dictionary that maps from street name (str) to list of arrival times (int)
    :return: total wait time (int)
    """
    #  schedule: ['rue-paris', 'rue-paris', 'rue-barcelone']
    cycle = [duration_ * [street] for street, duration_ in inters_schedule]
    factor = math.ceil(max_sim_time / len(cycle))
    schedule = factor * cycle
    schedule = [item for sublist in schedule for item in sublist]  # flatten list
    schedule = schedule[:max_sim_time]

    total_wait_time = 0
    street_to_num_waiting_cars_map = {}
    street_to_curr_arrival_idx_map = {street: 0 for street in street_to_arrival_times_map.keys()}
    for t, cur_green_street in enumerate(schedule):
        # let cars arrive
        for street_ in street_to_arrival_times_map.keys():
            if street_to_curr_arrival_idx_map[street_] < len(street_to_arrival_times_map[street_]) and street_to_curr_arrival_idx_map[street_] == t:
                if street_ in street_to_num_waiting_cars_map:
                    street_to_num_waiting_cars_map[street_] += 1
                else:
                    street_to_num_waiting_cars_map[street_] = 1
                street_to_curr_arrival_idx_map[street_] += 1

        # let car drive off
        if cur_green_street in street_to_num_waiting_cars_map and street_to_num_waiting_cars_map[cur_green_street] > 0:
            street_to_num_waiting_cars_map[cur_green_street] -= 1

        # compute wait time
        total_wait_time += sum(street_to_num_waiting_cars_map.values())

    return total_wait_time


if __name__ == '__main__':
    street_to_arrival_times_map = {
        'rue-paris': [0, 1],
        'rue-barcelone': [0]
    }

    schedule = [('rue-paris', 2), ('rue-barcelone', 1)]

    max_sim_time = 3

    print(compute_wait_time(street_to_arrival_times_map, schedule, max_sim_time))