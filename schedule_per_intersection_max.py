import math

def compute_wait_time(street_to_arrival_times_map: dict, inters_schedule: list, max_sim_time: int) -> int:
    """
    Computes the total waiting time of all cars at this intersection.

    :param street_to_arrival_times_map: A dictionary that maps from street name (str) to list of arrival times (int)
    :return: total wait time (int)
    """
    max_arrival_time = -1

    for street_name, arrival_times in street_to_arrival_times_map.items():
        max_arrival_time = max(arrival_times[-1], max_arrival_time)


    #  schedule: ['rue-paris', 'rue-paris', 'rue-barcelone']
    t = 0
    cycle = [duration * [street] for street, duration in inters_schedule]
    factor = math.ceil(max_sim_time / len(cycle))
    schedule = factor * cycle
    schedule = [item for sublist in schedule for item in sublist]  # flatten list
    schedule = schedule[:max_sim_time]

    total_wait_time = 0
    street_to_num_waiting_cars_map = {}
    for t, cur_green_street in enumerate(schedule):
        # let cars arrive
        for street_ in street_to_arrival_times_map.keys():
            if t in street_to_arrival_times_map[street_]:
                if street_ in street_to_num_waiting_cars_map:
                    street_to_num_waiting_cars_map[street_] += 1
                else:
                    street_to_num_waiting_cars_map[street_] = 1

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