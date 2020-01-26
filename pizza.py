from input import read_file
import numpy as np
import argparse

parser = argparse.ArgumentParser(description='pizza')

parser.add_argument('--input_file', type=str)

args = parser.parse_args()


nb_slice, list_pizza_slice = read_file(args.input_file)

# Sort in revert order
list_pizza_slice = list_pizza_slice[::-1]

total_slice = 0
current_indice = -1

while total_slice < nb_slice:
    current_indice += 1
    total_slice += list_pizza_slice[current_indice]



print("current_indice = ", current_indice)
print("total_slice = ", total_slice - list_pizza_slice[current_indice])
print("nb_slice = ", nb_slice)


