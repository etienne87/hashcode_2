def find_waiting_time(time, inter_schedule, street):
    """
    :param time: arrival time
    :param inters_schedule:
        [(rue-paris, 3), (rue-rome, 10)],
    :param street: street name
    :return:
    """
    cycle_length = sum([tf[1] for tf in inter_schedule])

    first_green =0
    time_green=None
    for tf_sch in inter_schedule:
        if tf_sch[0] == street:
            time_green = tf_sch[1]
            break
        first_green += tf_sch[1]

    if time_green is None:
        return -1

    time = time % cycle_length

    if time >= first_green + time_green:
        time = time - cycle_length

    if time <= first_green:
        return first_green - time
    if time < first_green + time_green:
        return 0




def car_timings(car, schedule, streets):
    """

    :param car: list de nom de rue
    :param schedule:
    {
        3: [(rue-paris, 3), (rue-rome, 10)],
        12: [(rue-paris, 3), (rue-rome2, 10)]
    }
    :return: [(id_inter1, arrival_time1), ... ]
    """

    time = 0
    car_times = []
    stopped = False
    for street in car:
        if street != car[0]:
            time += streets[street][2]
        id_inter = streets[street][1]

        if stopped:
            car_times.append((id_inter, 10000))
            break

        car_times.append((id_inter, time))

        if id_inter not in schedule.keys():
            stopped = True
        else:
            waiting_time = find_waiting_time(time, schedule[id_inter], street)
            if waiting_time < 0:
                stopped = True

        time += waiting_time

    return car_times



def compute_score(cars, schedule, streets, bonus, total_time):
    score = 0
    for car in cars:
        timings = car_timings(car,schedule,streets)
        arrival = timings[-1][1]
        if arrival < total_time:
            score += total_time - arrival + bonus

    return score
