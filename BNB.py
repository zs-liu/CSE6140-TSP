import argparse
from typing import Dict
import math
import numpy as np
import os
import sys
import time
import networkx as nx
from BranchState import BranchState

class BranchAndBound:
    def __init__(self, graph, limit=600):
        self.graph = graph
        self.winner = None
        self.results = []
        self.limit = limit

    def run_DFS(self, graph, matrix):
        stack = []
        initial_city = 1
        a = graph.copy()
        initial_state = BranchState(graph.copy(), [], 0, matrix)
        initial_state.add_stop(initial_city)
        stack.append(initial_state)
        i = 0

        while len(stack):
            if float(time.time()) - float(self.begin_time) > float(self.limit):
                break

            last_state = stack.pop()
            if not self.winner or last_state.bound_val < self.winner.bound_val:

                # checking for a candidate solution
                if len(graph.nodes.keys()) == len(last_state.path):

                    # checking if we have a cycle
                    if last_state.path[0] in graph[last_state.path[-1]].keys():
                        last_state.add_stop(last_state.path[0])

                        # checking if upper bound needs to be updated
                        if not self.winner or self.winner.bound_val > last_state.bound_val:
                            i += 1
                            self.results.append(
                                (last_state.path, last_state.path_cost, time.time() - self.begin_time))
                            print("Solution" + str(i) + ": ",
                                  (last_state.path, last_state.path_cost, time.time() - self.begin_time))
                            self.winner = last_state
                else:
                    sorted_list = self.sort_edges(graph[last_state.path[-1]])
                    for node, cost in sorted_list:
                        if node not in last_state.path:
                            new_state = BranchState(graph, last_state.path[:], last_state.path_cost,
                                                                matrix)
                            new_state.add_stop(node)

                            # checking if a branch can be pruned
                            if not self.winner or self.winner.bound_val > new_state.bound_val:
                                stack.append(new_state)

    def sort_edges(self, edge_dict):
        tup = []
        for key in edge_dict:
            tup.append((key, edge_dict[key]['weight']))

        sorted(tup, key=lambda edge: edge[1], reverse=True)

        return tup

    def generate_tour(self):
        graph = self.graph
        mat = [[0 for i in range(len(graph.nodes.keys()))] for j in range(len(graph.nodes.keys()))]
        for i in range(len(graph.nodes.keys())):
            for j in range(len(graph.nodes.keys())):
                if i != j:
                    mat[i][j] = graph[i + 1][j + 1]['weight']
                else:
                    mat[i][j] = sys.maxsize
        self.mat = np.array(mat)
        self.begin_time = time.time()
        self.run_DFS(graph, self.mat)

        return self.results

if __name__ == '__main__':
    # process arguments
    start = time.time()
    parser = argparse.ArgumentParser()
    parser.add_argument('-inf', action='store', dest='inf')
    parser.add_argument('-time', action='store', dest='time', default=1)
    parser.add_argument('-seed', action='store', dest='seed', default=0)
    args, unknown = parser.parse_known_args()
    # load graph
    # graph = Graph(args.inf)
    city_dict = {}
    with open(args.inf) as f:
        while True:
            line = f.readline()
            if 'NODE_COORD_SECTION\n' in line:
                break
        for line in f:
            if 'EOF\n' in line:
                break
            v = line.split(' ')
            city_dict[int(v[0])] = {'x': float(v[1]), 'y': float(v[2])}

    # building cost matrix for each edge
    graph = nx.Graph()
    for u in city_dict:
        for v in city_dict:
            if u != v:
                x_dist = city_dict[u]['x'] - city_dict[v]['x']
                y_dist = city_dict[u]['y'] - city_dict[v]['y']
                val = int(round(math.sqrt(x_dist ** 2 + y_dist ** 2)))
                graph.add_node(u)
                graph.add_node(v)
                graph.add_edge(u, v, weight=val)
    print(graph.number_of_nodes(), "nnnnnn")
    np.random.seed(int(args.seed))
    # test with relative path
    trace_file = '{}_{}_{}_{}.trace'.format('output/' + args.inf.split('/')[-1][:-4], 'BNB',
                                            args.time, args.seed)
    if os.path.isfile(trace_file):
        os.remove(trace_file)


    bnb = BranchAndBound(graph, args.time)
    tour = bnb.generate_tour()

    # output solution file
    solution_file = '{}_{}_{}_{}.sol'.format('output/' + args.inf.split('/')[-1][:-4], 'BNB',
                                             args.time, args.seed)
    with open(solution_file, 'w') as f:
        f.write(str(distance))
        f.write('\n')
        f.write(','.join(map(str, tour)))

    trace_file = '{}_{}_{}_{}.trace'.format('output/' + args.inf.split('/')[-1][:-4], 'BNB',
                                            args.time, args.seed)
    delta = time.time() - start
    with open(trace_file, 'a') as f:
        f.write('{:.2f}, {}\n'.format(delta, distance))

