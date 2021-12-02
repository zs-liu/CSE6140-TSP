import argparse
import math
import numpy as np
import os
import sys
import time
import networkx as nx
from branch_state import BranchState
from graph import Graph


class BranchAndBound:
    def __init__(self, g, start, solution_file, trace_file):
        self.g = g
        self.winner = None
        self.start = start
        self.solution_file = solution_file
        self.trace_file = trace_file

    def run_DFS(self, matrix):
        stack = []
        initial_city = 1
        initial_state = BranchState(self.g.copy(), [], 0, matrix)
        initial_state.add_stop(initial_city)
        stack.append(initial_state)
        i = 0

        have_solution = False
        while len(stack):

            last_state = stack.pop()
            if not self.winner or last_state.bound_val < self.winner.bound_val:

                # checking for a candidate solution
                if self.g.number_of_nodes() == len(last_state.path):

                    # checking if we have a cycle
                    if last_state.path[0] in graph[last_state.path[-1]].keys():
                        last_state.add_stop(last_state.path[0])

                        # checking if upper bound needs to be updated
                        if not self.winner or self.winner.bound_val > last_state.bound_val:
                            with open(self.solution_file, 'w+') as f:
                                f.write(str(last_state.path_cost))
                                f.write('\n')
                                f.write(','.join(map(str, last_state.path[:-1])))
                            delta = time.time() - self.start
                            if have_solution is False:
                                with open(self.trace_file, 'w') as f:
                                    pass
                                have_solution = True
                            with open(self.trace_file, 'a') as f:
                                f.write('{:.2f}, {}\n'.format(delta, last_state.path_cost))
                            self.winner = last_state
                else:
                    sorted_list = self.sort_edges(self.g[last_state.path[-1]])
                    for node, cost in sorted_list:
                        if node not in last_state.path:
                            new_state = BranchState(self.g.copy(), last_state.path[:], last_state.path_cost,
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
        mat = np.zeros((self.g.number_of_nodes(), self.g.number_of_nodes()))

        # generate a simple path to avoid no solution
        init_path = list(range(self.g.number_of_nodes()))
        init_cost = 0
        for x, y in zip(init_path, init_path[1:] + [0]):
            init_cost += self.g[x][y]['weight']
        with open(self.solution_file, 'w+') as f:
            f.write(str(init_cost))
            f.write('\n')
            f.write(','.join(map(str, init_path)))
        delta = time.time() - self.start
        with open(self.trace_file, 'a') as f:
            f.write('{:.2f}, {}\n'.format(delta, init_cost))

        for i in range(self.g.number_of_nodes()):
            for j in range(self.g.number_of_nodes()):
                if i != j:
                    try:
                        mat[i][j] = self.g[i][j]['weight']
                    except KeyError:
                        print(i, j)
                        raise KeyError
                else:
                    mat[i][j] = sys.maxsize
        self.run_DFS(np.array(mat))


if __name__ == '__main__':
    # process arguments
    start = time.time()
    parser = argparse.ArgumentParser()
    parser.add_argument('-inf', action='store', dest='inf')
    parser.add_argument('-time', action='store', dest='time', default=1)

    args, unknown = parser.parse_known_args()

    graph = Graph(args.inf)
    graph = nx.from_numpy_matrix(graph.distance)

    for u in range(graph.number_of_nodes()):
        for v in range(graph.number_of_nodes()):
            if u != v and not graph.has_edge(u, v):
                graph.add_edge(u, v, weight=0)

    solution_file = '{}_{}_{}.sol'.format('output/' + args.inf.split('/')[-1][:-4], 'BnB', args.time)
    trace_file = '{}_{}_{}.trace'.format('output/' + args.inf.split('/')[-1][:-4], 'BnB', args.time)

    bnb = BranchAndBound(graph, start=start, solution_file=solution_file, trace_file=trace_file)
    bnb.generate_tour()
