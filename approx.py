import argparse
import time
import numpy as np
import networkx as nx
from graph import Graph

if __name__ == '__main__':
    # process arguments

    start = time.time()
    parser = argparse.ArgumentParser()
    parser.add_argument('-inf', action='store', dest='inf')
    parser.add_argument('-time', action='store', dest='time', default=1)
    args, unknown = parser.parse_known_args()

    # load graph
    graph = Graph(args.inf)

    # generate graph from adjacency matrix
    g = nx.from_numpy_matrix(graph.distance)
    for u in range(g.number_of_nodes()):
        for v in range(g.number_of_nodes()):
            if u != v and not g.has_edge(u, v):
                g.add_edge(u, v, weight=0)
    # generate MST, default Kruskal’s algorithm
    mst = nx.minimum_spanning_tree(g)
    # generate nodes in a depth-first-search pre-ordering starting at node 0
    node_list = list(nx.dfs_preorder_nodes(mst, source=0))
    # calculate total distance
    length = 0
    for x, y in zip(node_list, node_list[1:] + [0]):
        length += graph[x, y]

    # calculate time consuming
    delta = time.time() - start

    # output solution file
    solution_file = '{}_{}_{}.sol'.format('output/' + args.inf.split('/')[-1][:-4], 'Approx', args.time)
    with open(solution_file, 'w') as f:
        f.write(str(length))
        f.write('\n')
        f.write(','.join(map(str, node_list)))

    # output trace file
    trace_file = '{}_{}_{}.trace'.format('output/' + args.inf.split('/')[-1][:-4], 'Approx', args.time)
    with open(trace_file, 'w') as f:
        f.write('{:.2f}, {}'.format(delta, length))
