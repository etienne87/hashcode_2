import numpy as np
import time
from read import read_file, write_file
import os




def build_dict_inters_car(list_cars, streets):
    full_dict_inters_car = {}
    for car in list_cars:
        for street_name in car[:-1]:
            id_inters_end_street = streets[street_name][1]
            if not id_inters_end_street in full_dict_inters_car:
                full_dict_inters_car[id_inters_end_street] = {}
            if street_name in full_dict_inters_car[id_inters_end_street]:
                full_dict_inters_car[id_inters_end_street][street_name] += 1
            else:
                full_dict_inters_car[id_inters_end_street][street_name] = 1

    return full_dict_inters_car


def build_dummy_schedule(full_dict_inters_car):

    dict_schedule_solution = {}
    for inters in full_dict_inters_car.keys():
        tab_nb_car = []
        list_name_street = list(full_dict_inters_car[inters].keys())
        for name_street in list_name_street:
            current_nb_car = full_dict_inters_car[inters][name_street]
            tab_nb_car.append(current_nb_car)

        minimum_nb_car = np.min(tab_nb_car)
        tab_nb_car_normalized = tab_nb_car/minimum_nb_car
        schedule = tab_nb_car_normalized.astype(np.int32)
        assert len(schedule) == len(list_name_street)
        dict_schedule_solution[inters] = []
        for ind_schedule in range(len(schedule)):
            current_street_name = list_name_street[ind_schedule]
            current_time_schedule = schedule[ind_schedule]
            dict_schedule_solution[inters].append((current_street_name, current_time_schedule))

    return dict_schedule_solution


def write_file_cheat(filename, intersection_dict):
    """
    # intersection_dict
    {
        3: [(rue-paris, 3), (rue-rome, 10)],
        12: [(rue-paris, 3), (rue-rome2, 10)]
    }
    """
    with open("output/{0}".format(filename), 'a') as the_file:
        the_file.truncate(0)
        the_file.write("{0} \n".format(len(intersection_dict))) # nbr intersection_dict
        for key, value in intersection_dict.items():
            the_file.write("{0} \n".format(key)) # intersection ID
            the_file.write("{0} \n".format(len(value))) # nbr street for schedule in intersection
            for value_car in value:
                the_file.write("{0} 1\n".format(value_car[0],value_car[1])) # for each street in the intersection : street_name time

def processFile(name_file):
    streets, cars, duration, nb_inters, nb_streets, nb_cars, bonus = read_file(os.path.join("input", name_file))
    list_cars = cars

    start_time = time.time()
    # print("time starting build_dict_inters_car = ", start_time)
    full_dict_inters_car = build_dict_inters_car(list_cars, streets)
    print("duration build_dict_inters_car = ", time.time()-start_time)
    start_time = time.time()
    dict_schedule_solution = build_dummy_schedule(full_dict_inters_car)
    print("duration build_dummy_schedule = ", time.time()-start_time)

    print("dict_schedule_solution = ", dict_schedule_solution)

    write_file_cheat(name_file, dict_schedule_solution)

name_files = [
"a.txt",
"b.txt",
"c.txt",
"d.txt",
"e.txt",
"f.txt"
]

for name in name_files:
  processFile(name)