import numpy as np

world = "TODO RAPH"
duration, nb_inters, nb_street, nb_car, bonus_point = world.get_all
list_inters = world.list_inters
list_street = world.list_street
list_cars = world.list_car

def build_dict_inters_car(list_inters, list_cars):
    full_dict_inters_car = {}
    for car in list_cars:
        for street in car.path_street:
            id_inters_end_street = street.end
            if not id_inters_end_street in full_dict_inters_car:
                full_dict_inters_car[id_inters_end_street] = {}
            if street.name in full_dict_inters_car[inters.id]:
                full_dict_inters_car[id_inters_end_street][street.name] += 1
            else:
                full_dict_inters_car[id_inters_end_street][street.name] = 1

    return full_dict_inters_car

def build_dummy_schedule(full_dict_inters_car, list_inters):

    for inters in list_inters:
        tab_nb_car = []
        list_name_street = full_dict_inters_car[inters.id].keys()
        for name_street in list_name_street:
            current_nb_car = full_dict_inters_car[inters.id][name_street]
            tab_nb_car.append(current_nb_car)

        minimum_nb_car = np.min(tab_nb_car)
        tab_nb_car_normalized = tab_nb_car/minimum_nb_car
        schedule = tab_nb_car_normalized.astype(np.int32)



for inters in list_inters:
    current_inters_list_street = inters.list_street
    nb_car_road_current_inters = np.zeros(len(current_inters_list_street))
    for street in inters.list_street:

