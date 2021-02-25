



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


if __name__ == '__main__':
    streets, cars, duration, nb_inters, nb_streets, nb_cars, bonus = read_file('input/a.txt')
    print(streets)
    print(cars)






























