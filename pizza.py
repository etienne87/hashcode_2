from input import read_file
from compute_score import compute_score
import numpy as np
import argparse

parser = argparse.ArgumentParser(description='pizza')

parser.add_argument('--input_file', type=str)

args = parser.parse_args()


nb_slice, list_pizza_slice = read_file(args.input_file)
orig_list_pizza_slice = list_pizza_slice.copy()

best_solution = nb_slice

for test_marin in range(0, 100):
    list_pizza_slice = orig_list_pizza_slice.copy()
    # Sort in revert order
    list_pizza_slice = list_pizza_slice[0:-test_marin]
    list_pizza_slice = list_pizza_slice[::-1]


    total_slice = 0
    list_indice_pizza = []

    for i, slice in enumerate(list_pizza_slice):
        if total_slice + slice <= nb_slice:
            total_slice += slice
            list_indice_pizza.append(i)

    if nb_slice - total_slice < best_solution:
        best_solution = nb_slice - total_slice
        print("we removed "+str(test_marin)+ "biggest pizza slice")
        print("total_slice = ", total_slice)
        print("len(list_indice_pizza) = ", len(list_indice_pizza))
        print("distance to optimal = ", nb_slice - total_slice)

    # score = compute_score(nb_slice, len(list_pizza_slice), list_pizza_slice, len(list_indice_pizza), list_indice_pizza)
    #
    # print("score Maximilian = ", score)
    # print("score optimal = ", nb_slice)
    # print("diff to optim = ", nb_slice - score)


