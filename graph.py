import numpy as np
from scipy.spatial import distance


class Graph:

    def __init__(self, file_path):
        with open(file_path) as f:
            # skip the header (5 lines) of the file
            for _ in range(5):
                next(f)
            # load coordinates from the file
            coords = []
            while (line := f.readline().strip()) != 'EOF':
                _, coord_x, coord_y = line.split(' ')
                coords.append((coord_x, coord_y))
        coords = np.array(coords)
        self._n = len(coords)
        # calculate distance
        self._distance = distance.cdist(coords, coords, 'euclidean')
        self._distance = np.rint(np.nextafter(self._distance, self._distance + 1)).astype('int')

    # get distance between two nodes
    def __getitem__(self, item) -> int:
        x, y = item
        return self._distance[x, y]

    # get total number of nodes
    @property
    def n(self) -> int:
        return self._n

    # get adjacency matrix
    @property
    def distance(self) -> np.array:
        return self._distance
