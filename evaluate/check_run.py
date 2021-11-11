import os
import subprocess
import pandas as pd


def _check_run(in_dir: str, out_dir: str, alg_name: str, timeout: int, run: bool, seed: int = None,
               instances: list = None) -> None:
    solutions = pd.read_csv(in_dir + 'solutions.csv')
    for _, row in solutions.iterrows():
        if instances is not None and not (row['Instance'] in instances):
            continue
        if seed is None:
            file = '{}_{}_{}.trace'.format(out_dir + row['Instance'], alg_name, timeout)
        else:
            file = '{}_{}_{}_{}.trace'.format(out_dir + row['Instance'], alg_name, timeout, seed)
        if os.path.isfile(file) is not True or run is True:
            subprocess.run(args=['python3', alg_name.lower() + '.py',
                                 '-inf', in_dir + row['Instance'] + '.tsp',
                                 '-time', str(timeout),
                                 '-seed', str(seed)],
                           timeout=timeout)
