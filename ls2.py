import argparse
import os
import time


from graph import Graph

if __name__ == '__main__':
    # process arguments

    print(os.getcwd())
    start = time.time()
    parser = argparse.ArgumentParser()
    parser.add_argument('-inf', action='store', dest='inf')
    parser.add_argument('-time', action='store', dest='time', default=1)
    args, unknown = parser.parse_known_args()

    # load graph
    graph = Graph(args.inf)
    # test with relative path
    # graph = Graph('DATA/Berlin.tsp')

    # set the initial tour from 0 to 0
    tour = list(range(0, graph.n)) + [0]
    num = graph.n

    distance = 0
    for k in range(num):
        distance += graph.distance[tour[k], tour[k + 1]]


    improved = True
    while improved:
        improved = False

        for i in range(num):
            for j in range(i + 2, num - 1):
                a = graph.distance[tour[i], tour[i + 1]]
                b = graph.distance[tour[j], tour[j + 1]]
                c = graph.distance[tour[i], tour[j]]
                d = graph.distance[tour[i+1], tour[j + 1]]

                check = c + d - a - b
                if check < 0:
                    tour = tour[0:i+1] + list(reversed(tour[i+1:j+1])) + tour[j+1:]
                    distance += check
                    improved = True

    print(distance)



    # calculate time consuming
    delta = time.time() - start


    # output solution file
    solution_file = '{}_{}_{}.sol'.format('output/' + args.inf.split('/')[-1][:-4], 'ls2', args.time)
    with open(solution_file, 'w') as f:
        f.write(str(distance))
        f.write('\n')
        f.write(','.join(map(str, tour)))

    # output trace file
    trace_file = '{}_{}_{}.trace'.format('output/' + args.inf.split('/')[-1][:-4], 'ls2', args.time)
    with open(trace_file, 'w') as f:
        f.write('{:.2f}, {}'.format(delta, distance))
