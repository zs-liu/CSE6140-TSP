import argparse
from graph import Graph

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-inf', action='store', dest='inf')
    parser.add_argument('-seed', action='store', dest='seed')

    args = parser.parse_args()

    graph = Graph(args.inf)