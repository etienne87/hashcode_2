
import numpy as np
from input import read_file


'''
------------------------------------------------
Use dynamic programming (DP) to solve 0/1 knapsack problem
Time complexity: O(nW), where n is number of items and W is capacity
------------------------------------------------
knapsack_dp(values,weights,n_items,capacity,return_all=False)
Input arguments:
  1. values: a list of numbers in either int or float, specifying the values of items
  2. weights: a list of int numbers specifying weights of items
  3. n_items: an int number indicating number of items
  4. capacity: an int number indicating the knapsack capacity
  5. return_all: whether return all info, defaulty is False (optional)
Return:
  1. picks: a list of numbers storing the positions of selected items
  2. max_val: maximum value (optional)
------------------------------------------------
'''

#https://dev.to/downey/solving-the-knapsack-problem-with-dynamic-programming-4hce





def sol_online(item_weights, max_weights):
    item_weights = [0] + item_weights
    item_values = item_weights
    print("item weights", item_weights)
    print(max_weights)
    n = len(item_weights)
    W = max_weights
    K = [[0 for w in range(W + 1)] for i in range(n)]

    # Recurrence
    for i in range(1, n):
      for w in range(1, W + 1):
        wi = item_weights[i]
        vi = item_values[i]

        if wi <= w:
          K[i][w] = max([K[i - 1][w - wi] + vi, K[i - 1][w]])
        else:
          K[i][w] = K[i - 1][w]

    # Results
    print("Result: ", K[n - 1][W])
    return K

    ## Optional: Uncomment to view the 2D table
    # from pandas import *
    # print("K table:")
    # print(DataFrame(K))






def main():
    max_slices, slices = read_file('input/d_quite_big.in')
    print("slices", slices)
    K_max_mem = 1000
    id_max = 0
    while slices[id_max] < K_max_mem:
        id_max += 1
        if id_max>= len(slices):
            break
    K = sol_online(slices, max_slices)
    print("max result", max_slices)



if __name__ == '__main__':
    main()

























