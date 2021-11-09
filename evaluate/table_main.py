import os
import subprocess
import numpy as np
import pandas as pd

ls_timeout = 600
ls_seed_list = list(range(0, 10))


def _check_run(in_dir, alg_name, timeout, run, seed=None) -> None:
    solutions = pd.read_csv(in_dir + 'solutions.csv')
    for _, row in solutions.iterrows():
        if seed is None:
            file = '{}_{}_{}.trace'.format(in_dir + row['Instance'], alg_name, timeout)
        else:
            file = '{}_{}_{}_{}.trace'.format(in_dir + row['Instance'], alg_name, timeout, seed)
        if os.path.isfile(file) is not True or run is True:
            subprocess.run(args=['python3', alg_name.lower() + '.py',
                                 '-inf', in_dir + row['Instance'] + '.tsp',
                                 '-time', str(timeout),
                                 '-seed', str(seed)],
                           timeout=timeout)


def _get_result(in_dir, alg_name, timeout, seed=None) -> pd.DataFrame:
    solutions = pd.read_csv(in_dir + 'solutions.csv')
    solutions = solutions.assign(_time=np.nan, _qual=0, _error=np.nan)
    for idx, row in solutions.iterrows():
        if seed is None:
            file = '{}_{}_{}.trace'.format(in_dir + row['Instance'], alg_name, timeout)
        else:
            file = '{}_{}_{}_{}.trace'.format(in_dir + row['Instance'], alg_name, timeout, seed)
        with open(file) as f:
            for line in f:
                pass
            last_line = line.strip()
            _time, _qual = last_line.split(', ')
            solutions.loc[idx, '_time'] = float(_time)
            solutions.loc[idx, '_qual'] = int(_qual)
            solutions.loc[idx, '_error'] = (int(_qual) - row['Value']) / row['Value']
    return solutions


def _output_table(output_file: str, table: pd.DataFrame):
    with open(output_file, 'w') as f:
        f.write(table.to_latex(index=False,
                               header=['Dataset', 'Optimal solution', 'Running time',
                                       'Solution quality', 'Relative error'],
                               formatters={'_time': '{:0.2f}'.format,
                                           '_qual': '{:0.0f}'.format,
                                           '_error': '{:0.4f}'.format},
                               column_format='lllll'))


def table_out(in_dir, out_dir, alg, run):
    if 'bnb' in alg:
        _check_run(in_dir=in_dir, alg_name='BnB', timeout=600, run=run, seed=None)
        solutions = _get_result(in_dir=in_dir, alg_name='BnB', timeout=600, seed=None)
        output_file = out_dir + 'bnb_table.tex'
        _output_table(output_file, solutions)

    if 'approx' in alg:
        _check_run(in_dir=in_dir, alg_name='Approx', timeout=1, run=run, seed=None)
        solutions = _get_result(in_dir=in_dir, alg_name='Approx', timeout=1, seed=None)
        output_file = out_dir + 'approx_table.tex'
        _output_table(output_file, solutions)

    if 'ls1' in alg:
        for seed in ls_seed_list:
            _check_run(in_dir=in_dir, alg_name='LS1', timeout=ls_timeout, run=run, seed=seed)
        solutions = pd.read_csv(in_dir + 'solutions.csv')
        solutions = solutions.assign(_time=0.0, _qual=0.0, _error=0.0)
        for seed in ls_seed_list:
            _solutions = _get_result(in_dir=in_dir, alg_name='LS1', timeout=ls_timeout, seed=seed)
            solutions['_time'] += _solutions['_time']
            solutions['_qual'] += _solutions['_qual']
            solutions['_error'] += _solutions['_error']
        solutions['_time'] /= len(ls_seed_list)
        solutions['_qual'] /= len(ls_seed_list)
        solutions['_error'] /= len(ls_seed_list)
        output_file = out_dir + 'ls1.tex'
        _output_table(output_file, solutions)
    if 'ls2' in alg:
        for seed in ls_seed_list:
            _check_run(in_dir=in_dir, alg_name='LS2', timeout=ls_timeout, run=run, seed=seed)
        solutions = pd.read_csv(in_dir + 'solutions.csv')
        solutions = solutions.assign(_time=0.0, _qual=0.0, _error=0.0)
        for seed in ls_seed_list:
            _solutions = _get_result(in_dir=in_dir, alg_name='LS2', timeout=ls_timeout, seed=seed)
            solutions['_time'] += _solutions['_time']
            solutions['_qual'] += _solutions['_qual']
            solutions['_error'] += _solutions['_error']
        solutions['_time'] /= len(ls_seed_list)
        solutions['_qual'] /= len(ls_seed_list)
        solutions['_error'] /= len(ls_seed_list)
        output_file = out_dir + 'ls2.tex'
        _output_table(output_file, solutions)
