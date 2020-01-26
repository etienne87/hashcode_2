

def read_file(filename):
    with open(filename, 'r') as f:
        max_slices, _ = f.readline().split(' ')
        slices = f.readline().split(' ')  
        slices = [int(item) for item in slices]              
        return max_slices, slices

if __name__ == '__main__':
    max_slices, slices = read_file('input/c_medium.in')

    print(max_slices)
    print(slices)