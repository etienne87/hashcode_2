from input import read_file


def optimize_max_slices(slices, max_possible):
    total = 0
    ans = []
    for v in slices[::-1]:
        if (total + v) < max_possible:
            ans.append(v)
            total += v
        
        if total >= max_possible:
            break
    return ans, total

if __name__ == '__main__':
    max_slices, slices = read_file('input/e_also_big.in')

    ans, total = optimize_max_slices(slices, max_slices)
    print(total, max_slices)
