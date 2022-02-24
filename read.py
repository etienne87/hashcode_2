from types import SimpleNamespace

def read_file(filename):
    r = SimpleNamespace()
    with open(filename, 'r') as f:
        r.c, r.p = [int(x) for x in f.readline().strip()]
        r.L = []
        r.D = []
        for client_num in range(r.C):
            r.L.append(list(set([str(x) for x in f.readline().strip().split(' ')[1:]])))
            r.D.append(list(set([str(x) for x in f.readline().strip().split(' ')[1:]])))

        r.L_ingredients = set.union(*[set(x) for x in r.L])
        r.D_ingredients = set.union(*[set(x) for x in r.D])
        r.ingredients = r.L_ingredients.union(r.D_ingredients)

    return r


if __name__ == '__main__':
    r = read_file('input/a_an_example.in.txt')
    print(r)
