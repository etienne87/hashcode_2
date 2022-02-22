"""
Python Dijkstra: super slow...
"""
import numpy as np
import heapq
import itertools
from collections import namedtuple
from functools import partial


def my_dijkstra(matrix, start, end):
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
    
    modu = int(0.2 * x_max*y_max*z_max)

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
        
        
        if certain.sum()%modu == 0: 
            print('ratio: ', 100 * certain.sum() / (x_max*y_max*z_max), '%')
    
    ## retrieve the path
    cur_x, cur_y, cur_z = xn, yn, zn 
    # Create Tour
    tour = []
    tour += [[xn,yn,zn]]
    while (cur_x, cur_y, cur_z) != (x0, y0, z0):
        cur_x, cur_y, cur_z = transitions[(cur_x, cur_y, cur_z)]
        tour += [[cur_x,cur_y,cur_z]]
    return np.array(tour)
