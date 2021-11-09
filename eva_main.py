import subprocess
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-out', action='store', dest='out', default='table', choices=['table', 'qrtd', 'sqd', 'box'])
    parser.add_argument('-i', action='store', dest='i', default='DATA/')
    parser.add_argument('-o', action='store', dest='o', default='OUT/')
    parser.add_argument('-run', action='store', dest='run', default='F', choices=['T', 'F'])
    parser.add_argument('-alg', action='store', dest='alg', default='all', choices=['BnB', 'Approx', 'LS1', 'LS2', 'all'])
    args, unknown = parser.parse_known_args()

    if args.run == 'T':
        args.run = True
    else:
        args.run = False
    if args.alg == 'all':
        args.alg = [x.lower() for x in ['BnB', 'Approx', 'LS1', 'LS2']]
    else:
        args.alg = [args.alg.lower()]

    if args.out == 'table':
        from evaluate.table_main import table_out
        table_out(in_dir=args.i, out_dir=args.o, alg=args.alg, run=args.run)
    elif args.out == 'grtd':
        pass
