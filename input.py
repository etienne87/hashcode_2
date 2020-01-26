

def read_file(filename):
    with open(filename, 'r') as f:
        max_slices, _ = f.readline().split(' ')
        slices = f.readline().split(' ')  
        slices = [int(item) for item in slices]              
        return int(max_slices), slices

if __name__ == '__main__':
    max_slices, slices = read_file('input/e_also_big.in')
    import pdb;pdb.set_trace()
    print(max_slices)
    print(slices)