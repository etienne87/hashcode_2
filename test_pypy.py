import time
#from scipy.optimize import linear_sum_assignement
from types import SimpleNamespace

def create(n):
    objs = []
    for i in range(n):
        obj = SimpleNamespace()
        obj.x = 0
        obj.y = 45
        obj.z = 2*i
        objs.append(obj)
    return objs

def polynomial(objs):
    n = len(objs)
    s = 0
    for i in range(n):
        for j in range(n):
            for k in range(n):
                s += objs[i].x*objs[j].y*objs[k].z 
    return s


def example_from_web():
    total = 0
    for i in range(1, 10000):
        for j in range(1, 10000):
            total += i + j
    

def test(n):
    print(n)
    objs = create(n)
    print('n: ', len(objs))
    polynomial(objs)


def fibo(n):
    if n == 0:
        return 0
    elif n == 1 or n == 2:
        return 1
    else:
        return fibo(n-1) + fibo(n-2)


def stack(n):
    stack = []
    for i in range(n):
        stack.append(i)
    for i in range(n):
        stack.pop()
    return stack


def main(program, n):
    fun = globals()[program]
    t1 = time.time()
    fun(n)
    t2 = time.time()
    print(t2-t1, ' s')



if __name__ == '__main__':
    import fire;fire.Fire(main)

