



def read_file(filename):
    with open(filename, 'r') as f:
        duration, nb_inters, nb_streets, nb_cars, bonus = f.readline().rstrip("\n").split(' ')

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
            for value_car in value:
                the_file.write("{0} {1}\n".format(value_car[0],value_car[1])) # for each street in the intersection : street_name time


if __name__ == '__main__':
    streets, cars, duration, nb_inters, nb_streets, nb_cars, bonus = read_file('input/a.txt')
    print(streets)
    print(cars)
    write_file('a.txt',{1: [('rue-paris', 3), ('rue-rome', 10)] ,2: [('rue-paris', 3), ('rue-rome2', 10)]})






























