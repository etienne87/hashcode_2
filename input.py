

def read_file(filename):
    with open(filename, 'r') as f:
        N, M = f.readline().split(' ')
        slices = f.readline().split(' ')  
        slices = [int(item) for item in slices]              
        return N, M, slices

if __name__ == '__main__':
    n,m, slices = read_file('input/c_medium.in')

    print(n, m)
    print(slices)