import argparse
import numpy as np
import os
import time
import random
import math

from graph import Graph

def getDistance(path):
    res = 0
    for i in range(num - 1):
        res += graph[path[i], path[i + 1]]
    res += graph[path[num - 1], path[0]]
    return res
        
def getNewpath(cur_path, num):
    i = random.randint(0, num-1)          # create the first int in [0,n) 
    while True:
        j = random.randint(0, num-1)      # create an int in [0,n)
        if i!=j: break                      # ensure i, j are not the same
    path = cur_path.copy()            
    path[i], path[j] = cur_path[j], cur_path[i] # change location i and j
    return path
    
if __name__ == '__main__':
    # process arguments 

    start = time.time()
    parser = argparse.ArgumentParser()
    parser.add_argument('-inf', action='store', dest='inf')
    parser.add_argument('-time', action='store', dest='time', default=1)
    parser.add_argument('-seed', action='store', dest='seed', default=0)
    args, unknown = parser.parse_known_args()

    # load graph
    # args.inf = "Atlanta.tsp"
    # print(args.inf)
    # args.time = 600
    # args.seed = 1
    graph = Graph(args.inf) 
    np.random.seed(int(args.seed))
    # test with relative path
    # graph = Graph('DATA/Berlin.tsp')
    
    L = 1000 
    T = 1e10 # initial temperature
    Tend = 1e-9
    rate = 0.99 # cooling rate
    num = graph.n # the number of locations
    random.seed(args.seed)
    cur_path = random.sample(range(0, num), num) # get initial solution
    
    cur_dis = getDistance(cur_path) # get initial distance
    best_path = cur_path # initialize best path
    best_dis = cur_dis # initialize best distance
    t = T   
    
    trace_file = '{}_{}_{}_{}.trace'.format('output/' + args.inf.split('/')[-1][:-4], 'LS1',
                                            args.time, args.seed)
    if os.path.isfile(trace_file):
        os.remove(trace_file)

    not_improved = 0
    while not_improved < 10:
        improved = False
        for point in range(L):
            new_path = getNewpath(cur_path, num)
            new_dis = getDistance(new_path)
            D = new_dis - cur_dis
            if t <= Tend and cur_dis <= best_dis:
                t = T
            if D < 0:
                cur_path = new_path
                cur_dis = new_dis
                if best_dis > cur_dis:
                    best_dis = cur_dis
                    best_path = cur_path  
                    improved = True
            else:
                p = math.exp(-D/t)
                if random.random() < p: # accept this result
                    cur_path = new_path
                    cur_dis = new_dis

            t = max(t * rate, Tend * 0.1)
            
        if improved:
            not_improved = 0
            # output solution file
            solution_file = '{}_{}_{}_{}.sol'.format('output/' + args.inf.split('/')[-1][:-4], 'LS1',
                                                    args.time, args.seed)
            with open(solution_file, 'w+') as f:
                f.write(str(best_dis))
                f.write('\n')
                f.write(','.join(map(str, best_path)))

            # output trace file
            trace_file = '{}_{}_{}_{}.trace'.format('output/' + args.inf.split('/')[-1][:-4], 'LS1',
                                                args.time, args.seed)
            delta = time.time() - start
            with open(trace_file, 'a') as f:
                f.write('{:.2f}, {}\n'.format(delta, best_dis))
        else:
            not_improved += 1
        