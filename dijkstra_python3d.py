"""
Python Dijkstra: super slow...
"""
import numpy as np
import heapq


def dijkstra3d(matrix, start, end):
    """
    Implementation of Dijkstra algorithm to find the (s,t)-shortest path between top-left and bottom-right nodes
    on a n^3 grid graph (with 26-neighbourhood).
    This is only for pedagogic purpose. We call a more efficiently implementation.
    NOTE: This is an vertex variant of the problem, i.e. nodes carry weights, not edges.
    Args:
        volume (np.ndarray [grid_dim, grid_dim, grid_dim]): Matrix of node-costs.
        on_path volume (np.ndarray [grid_dim, grid_dim, grid_dim]), indicator matrix of nodes on the shortest path.
        start (tuple): start position
        end (tuple): end position
    """
    x0, y0, z0 = start[0], start[1], start[2]
    xn, yn, zn = end[0], end[1], end[2]
    x_max, y_max, z_max = matrix.shape

    costs = np.full_like(matrix, np.inf)
    costs[x0,y0,z0] = matrix[x0,y0,z0]

    priority_queue = [(matrix[x0,y0,z0], (x0, y0, z0))]

    certain = np.zeros((x_max,y_max,z_max), dtype=np.uint8)
    certain[x0,y0,z0] = 1
    transitions = dict()

    #modu = int(0.2 * x_max*y_max*z_max)

    while priority_queue:
        cur_cost, (cur_x, cur_y, cur_z) = heapq.heappop(priority_queue)
        if certain[cur_x,cur_y,cur_z]:
            pass

        for dx in (-1,0,1):
            for dy in (-1,0,1):
                for dz in (-1,0,1):
                    x, y, z = cur_x + dx, cur_y + dy, cur_z + dz
                    if (0 <= x < x_max) and (0 <= y < y_max) and (0 <= z < z_max) and (dx, dy, dz) != (0, 0, 0) and not certain[x,y,z]:
                        # heuristic cost: euclidean distance
                        heuristic_cost = np.sqrt( (x-xn)**2 + (y-yn)**2 + (z-zn)**2 )
                        priority = matrix[x,y,z] + costs[cur_x,cur_y,cur_z] + heuristic_cost
                        if matrix[x,y,z] + costs[cur_x,cur_y,cur_z] < costs[x,y,z]:
                            costs[x,y,z] = matrix[x,y,z] + costs[cur_x,cur_y,cur_z]
                            heapq.heappush(priority_queue, (priority, (x, y, z)))
                            transitions[(x, y, z)] = (cur_x, cur_y, cur_z)

        certain[cur_x,cur_y,cur_z] = 1


        #if certain.sum()%modu == 0:
        #    print('ratio: ', 100 * certain.sum() / (x_max*y_max*z_max), '%')

    ## retrieve the path
    cur_x, cur_y, cur_z = xn, yn, zn
    # Create Tour
    tour = []
    tour += [[xn,yn,zn]]
    while (cur_x, cur_y, cur_z) != (x0, y0, z0):
        cur_x, cur_y, cur_z = transitions[(cur_x, cur_y, cur_z)]
        tour += [[cur_x,cur_y,cur_z]]
    return np.array(tour)

def define_path(s, n=50, k=3):
    weights = np.random.randn(s,s,s) + 100
    path = np.zeros((s,s,s), dtype=np.uint8)
    start = (0,0,0)
    path[start[0],start[1],start[2]] = 1
    dir = np.random.uniform(-1,1, (3,))
    dir = dir/np.sqrt((dir**2).sum())
    alpha = 0.9
    cur = start
    trans = [start]
    for j in range(k):
        for i in range(n):
            cur = (cur + dir).astype(np.int32)
            if cur[0] >= s or cur[1] >= s or cur[2] >= s:
                break
            if not (cur == trans[-1]).all():
                path[cur[0],cur[1],cur[2]] = 1
                weights[cur[0],cur[1],cur[2]] = 1
                if i == 0:
                    trans.append(cur)
            dir = dir * alpha + np.random.uniform(-1,1, (3,)) * (1-alpha)
    return weights, path, np.array(trans)



def main(size):
    import time
    weights, dense, path = define_path(size, 100, 100)
    start = np.random.randint(0, size-1, (3,)).tolist()
    start = path[0]
    end = path[-1]
    print(path.shape, weights.shape, start, end)

    t1 = time.time()
    tour = dijkstra3d(weights, start, end)
    t2 = time.time()
    print(f'runtime: {t2-t1}')

if __name__ == '__main__':
    import fire;fire.Fire(main)
