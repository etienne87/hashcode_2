import os, glob
from input import read_file
from compute_score import compute_score

def optimize_max_slices(slices, max_possible):
    total = 0
    ans = []
    for i, v in enumerate(slices[::-1]):
        if (total + v) < max_possible:
            ans.append(i)
            total += v
        
    return ans, total

def run_all(dir):
    total = 0
    filenames = glob.glob(dir + "/*.in")
    print(filenames)
    for filename in filenames:
        max_slices, slices = read_file(filename)
        total_pizza_types = len(slices)
        ans, total = optimize_max_slices(slices, max_slices)
        print("problem: ", os.path.basename(filename), ": ", total, max_slices, max_slices-total)
        score = compute_score(max_slices, total_pizza_types, slices, len(ans), ans)
        total += score
    return total

if __name__ == '__main__':

    # max_slices, slices = read_file('input/d_also_big.in')
    # total_pizza_types = len(slices)
    # ans, total = optimize_max_slices(slices, max_slices)
    # print(total, max_slices, max_slices-total)
    # score = compute_score(max_slices, total_pizza_types, slices, len(ans), ans)
    # print(score)

    score = run_all('input')

    print('total score: ', score)