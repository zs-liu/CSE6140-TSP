import argparse
import numpy as np
import os
import time

from graph import Graph

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

    trace_file = '{}_{}_{}_{}.trace'.format('output/' + args.inf.split('/')[-1][:-4], 'ls2',
                                            args.time, args.seed)
    if os.path.isfile(trace_file):
        os.remove(trace_file)

    # set the initial tour from 0 to 0
    tour = list(np.random.permutation(list(range(0, graph.n))))
    # tour = list(range(0, graph.n))

    tour = tour + [tour[0]]
    num = graph.n
    
    def getdistmat(coordinates):
        num = coordinates.shape[0] 
        distmat = np.zeros((graph.n,graph.n)) 
        for i in range(num):
            for j in range(i,num):
                distmat[i][j] = distmat[j][i]=np.linalg.norm(coordinates[i]-coordinates[j])
            return distmat
    
    def initpara():
        rate = 0.99 # cooling rate
        t = (1,100)
        T = 1000 # temperature
        return rate,t,T
    
    num = graph.coordinates.shape[0]
    distmat = getdistmat(graph.coordinates) # obtain a matirx of distance
    
    new_solution = np.arange(num)
    current_solution = new_solution.copy()
    current_distance =99000  # set a relatively large number as an initial value
    #print(valuecurrent)
 
    best_solution = new_solution.copy()
    best_distance = 99000 #np.max
 
    rate, t2, T = initpara()
    t = t2[1]
    
    while t > t2[0]:
        for i in np.arange(T):
            if np.random.rand() > 0.5:# exchange the sequence of the two numbers 
            # np.random.rand() produce random numbers between [0, 1)
                while True: # produce two random numbers
                    loc1 = np.int(np.ceil(np.random.rand()*(num-1)))
                    loc2 = np.int(np.ceil(np.random.rand()*(num-1)))
                ## print(loc1,loc2)
                    if loc1 != loc2:
                         break
                new_solution[loc1],new_solution[loc2] = new_solution[loc2],new_solution[loc1]
            else: 
                while True:
                    loc1 = np.int(np.ceil(np.random.rand()*(num-1)))
                    loc2 = np.int(np.ceil(np.random.rand()*(num-1))) 
                    loc3 = np.int(np.ceil(np.random.rand()*(num-1)))
 
                    if((loc1 != loc2)&(loc2 != loc3)&(loc1 != loc3)):
                        break
                
                if loc1 > loc2:
                    loc1,loc2 = loc2,loc1
                if loc2 > loc3:
                    loc2,loc3 = loc3,loc2
                if loc1 > loc2:
                    loc1,loc2 = loc2,loc1
 
                tmplist = new_solution[loc1:loc2].copy()
                new_solution[loc1:loc3-loc2+1+loc1] = new_solution[loc2:loc3+1].copy()
                new_solution[loc3-loc2+1+loc1:loc3+1] = tmplist.copy()  
            
            distance = 0    
        for i in range(num-1):
            distance += distmat[new_solution[i]][new_solution[i+1]]
            distance += distmat[new_solution[0]][new_solution[num-1]]
            # print (distance)
            if distance < current_distance: # accept the solution
           
            # update current_solution and best_solution
                current_distance = distance
                current_solution = new_solution.copy()
 
                if distance < best_distance:
                    best_distance = distance
                    best_solution = new_solution.copy()
        else: # Accept the solution at some probability
            if np.random.rand() < np.exp(-(distance-current_distance)/t):
                current_distance = distance
                current_solution = new_solution.copy()
            else:
                new_solution = current_solution.copy()
        t = rate * t
        tour.append(best_distance)
        print (t)
    
        # output solution file
        solution_file = '{}_{}_{}_{}.sol'.format('output/' + args.inf.split('/')[-1][:-4], 'LS1',
                                                     args.time, args.seed)
        with open(solution_file, 'w+') as f:
            f.write(str(distance))
            f.write('\n')
            f.write(','.join(map(str, tour)))

        # output trace file
            trace_file = '{}_{}_{}_{}.trace'.format('output/' + args.inf.split('/')[-1][:-4], 'LS1',
                                                    args.time, args.seed)
            delta = time.time() - start
            with open(trace_file, 'a') as f:
                f.write('{:.2f}, {}\n'.format(delta, distance))