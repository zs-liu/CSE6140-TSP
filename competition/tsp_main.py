import subprocess
import argparse
import os

if __name__ == '__main__':
    
    if not os.path.exists('output/'):
        os.makedirs('output/')

    parser = argparse.ArgumentParser()
    parser.add_argument('-inst', action='store', dest='inf')
    parser.add_argument('-alg', action='store', dest='alg', default='LS', choices=['LS'])
    parser.add_argument('-time', action='store', dest='time', default=10)
    parser.add_argument('-seed', action='store', dest='seed', default=None)
    args, unknown = parser.parse_known_args()

    try:
        subprocess.run(args=['python3', str(args.alg).lower() + '.py',
                             '-inf', str(args.inf),
                             '-time', str(args.time),
                             '-seed', str(args.seed)],
                       timeout=int(args.time))
    except subprocess.TimeoutExpired:
        pass
