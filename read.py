
from functools import *
from math import *


def read_file(filename):
    with open(filename, 'r') as f:
        duration, nb_inters, nb_streets, nb_cars, bonus = f.readline().rstrip("\n").split(' ')
        print("duration {0}".format(duration))
        print("nb_inters {0}".format(nb_inters))
        print("nb_streets {0}".format(nb_streets))
        print("nb_cars {0}".format(nb_cars))
        print("bonus {0}".format(bonus))


        streets = {}
        for i in range(int(nb_streets)):
            start, end, name, length = f.readline().rstrip("\n").split(' ')
            streets[name] = (int(start), int(end), int(length))

        cars = []
        for i in range(int(nb_cars)):
          car_desc = f.readline().rstrip("\n").split(' ')
          nb_streets = car_desc[0]
          path = car_desc[1:]
          cars.append(path)



    return streets, cars, duration, nb_inters, nb_streets, nb_cars, bonus


def write_file(filename, intersection_dict):
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
            for value_car in sorted(value, key = lambda i: i[1]):
                the_file.write("{0} {1}\n".format(value_car[0],value_car[1])) # for each street in the intersection : street_name time

def write_file_normer(filename, intersection_dict,nombre_magic):
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
            nbr_intersection = len(value)
            total_time_schedule = reduce(lambda x,y:x+int(y[1]), value,0)
            max_time_schedule = floor(nbr_intersection * nombre_magic)
            for value_car in sorted(value, key = lambda i: i[1]):
                the_file.write("{0} {1}\n".format(value_car[0], ceil(value_car[1] * max_time_schedule / total_time_schedule))) # for each street in the intersection : street_name time

if __name__ == '__main__':
    streets, cars, duration, nb_inters, nb_streets, nb_cars, bonus = read_file('input/a.txt')
    print(streets)
    print(cars)
    write_file('a.txt',{1: [('rue-paris', 3), ('rue-rome', 10)] ,2: [('rue-paris', 3), ('rue-rome2', 10)]})






























