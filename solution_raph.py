
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
    K = [[[0,[]] for w in range(W + 1)] for i in range(n)]

    # Recurrence
    for i in range(1, n):
      for w in range(1, W + 1):
        wi = item_weights[i]
        vi = item_values[i]

        if wi <= w:
          if K[i - 1][w - wi][0] + vi > K[i - 1][w][0]:
              K[i][w][0] = K[i - 1][w - wi][0] + vi
              K[i][w][1] = K[i - 1][w - wi][1] + [i-1]
          else:
              K[i][w] =  K[i - 1][w]
        else:
          K[i][w] = K[i - 1][w]

    # Results
    print("Result: ", K[n - 1][W][0])
    print(K[n - 1][W])
    return K

    ## Optional: Uncomment to view the 2D table
    # from pandas import *
    # print("K table:")
    # print(DataFrame(K))






def main():
    max_slices, slices = read_file('input/d_quite_big.in')
    print("slices", slices)
    K_max_mem = 10000
    id_max_mem = 0
    while slices[id_max_mem] < K_max_mem:
        id_max_mem += 1
        if id_max_mem >= len(slices):
            break
    K = sol_online(slices[:id_max_mem], K_max_mem)
    big_slices = slices[id_max_mem:]
    len_big = len(big_slices)
    available = np.ones(len_big)

    current_size = 0
    list_id_pizza = []

    while current_size < max_slices-K_max_mem:
        if np.alltrue(available==0):
            break
        possib = np.where(available==1)[0]
        id_id = np.random.randint(0, len(possib))
        id_next = possib[id_id]
        available[id_next] = 0
        if big_slices[id_next] > max_slices - current_size:
            pass
        else:
            current_size += big_slices[id_next]
            list_id_pizza += [id_next + id_max_mem]


    print("hellloooo", max_slices-current_size)

#    K = sol_online(slices[:id_max_mem], max_slices - K_max_mem)






    print("max result", max_slices)



if __name__ == '__main__':
    main()

























