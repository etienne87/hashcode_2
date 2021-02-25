import numpy as np
import math
from read import read_file, write_file


def compute_solution(filename):
    streets, cars, duration, nb_inters, nb_streets, nb_cars, bonus = read_file(f'input/{filename}.txt')

    # Dict from street name (str) to number of car passages (int)
    street_stats = {}
    for car_path in cars:
        for street in car_path[:-1]:
            if street in street_stats:
                street_stats[street] += 1
            else:
                street_stats[street] = 1

    # Build a list of intersections
    intersections = {}
    # Each intersection is represented by a list of tuples [(street name, time)]
    for street_name, values in streets.items():
        inters_depart, inters_arrival, time = values
        if street_name in street_stats:
            if inters_arrival in intersections:
                # assert street_name not in solution_intersections[inters_arrival]
                intersections[inters_arrival].append((street_name, street_stats[street_name]))
            else:
                intersections[inters_arrival] = [(street_name, street_stats[street_name])]

    # normalize
    for intersection_id, streets in intersections.items():
        min_time = np.inf
        for street_name, time in streets:
            min_time = min(time, min_time)

        for street_id, (street_name, time) in enumerate(streets):
            streets[street_id] = (street_name, math.ceil(time / min_time))


    write_file(f'{filename}.txt', intersections)


if __name__ == '__main__':
    for filename in ['a', 'b', 'c', 'd', 'e']:
        compute_solution(filename)

