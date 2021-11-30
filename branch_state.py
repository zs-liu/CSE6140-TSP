import networkx as nx
import numpy as np
import sys


class BranchState:

    def __init__(self, graph, path, path_cost, matrix):
        self.graph = graph
        self.path = path
        self.path_cost = path_cost
        self.matrix = matrix

    def add_stop(self, stop):
        if len(self.path):
            self.path_cost = self.path_cost + self.graph[self.path[-1]][stop]['weight']
        self.path.append(stop)
        self.bound_val = self.get_min_dist_lower_bound(self.matrix, self.path, self.path_cost)

    def get_min_dist_lower_bound(self, matrix, path, path_cost):
        mat = matrix.copy()
        if len(path) > 1:
            i = 0
            while i < len(path) - 2:
                mat[path[i]] = sys.maxsize
                mat[path[i + 1]] = sys.maxsize
                i += 2
        row_min = np.amin(mat, axis=1)
        mat = mat - np.reshape(row_min, (len(matrix), 1))
        col_min = np.amin(mat, axis=0)

        return np.sum(row_min) + np.sum(col_min) + path_cost
