import numpy as np


def compute_score(max_slices, types_of_pizza, slices_per_pizza, num_ordered_pizzas, ordered_pizzas_idx, verbose=False):
    if num_ordered_pizzas > types_of_pizza:
        raise ValueError('You ordered more pizzas that exist')

    ordered_slices = sum(np.array(slices_per_pizza)[np.array(ordered_pizzas_idx)])

    if ordered_slices > max_slices:
        raise ValueError('You ordered more than the maximum number of slices')

    if verbose:
        print('Score: {}'.format(ordered_slices))
    else:
        return ordered_slices


if __name__ == '__main__':
    compute_score(17, 4, [2, 5, 6, 8], 3, [0, 2, 3])