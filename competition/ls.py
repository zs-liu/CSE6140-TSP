import argparse
import numpy as np
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
    graph = Graph(args.inf)
    np.random.seed(int(args.seed))

    # output path
    solution_file = '{}_{}_{}_{}.sol'.format('output/' + args.inf.split('/')[-1][:-4], 'LS',
                                             args.time, args.seed)
    trace_file = '{}_{}_{}_{}.trace'.format('output/' + args.inf.split('/')[-1][:-4], 'LS',
                                            args.time, args.seed)

    best = None
    while True:
        # set a random initial tour
        tour = list(np.random.permutation(list(range(0, graph.n))))

        tour = tour + [tour[0]]
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
                    d = graph.distance[tour[i + 1], tour[j + 1]]

                    check = c + d - a - b
                    if check < 0:
                        tour = tour[0:i + 1] + list(reversed(tour[i + 1:j + 1])) + tour[j + 1:]
                        distance += check
                        improved = True
            # output solution file
            if improved and (best is None or best > distance):
                best = distance
                with open(solution_file, 'w') as f:
                    f.write(str(distance))
                    f.write('\n')
                    f.write(','.join(map(str, tour[:-1])))

                delta = time.time() - start
                with open(trace_file, 'a') as f:
                    f.write('{:.2f}, {}\n'.format(delta, distance))
