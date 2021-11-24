import os
import numpy as np
import pandas as pd
from evaluate import _check_run
from .parameters import ls_timeout, ls_seed_list


def _get_result(in_dir: str, out_dir: str, alg_name: str, timeout: int, seed: int = None) -> pd.DataFrame:
    solutions = pd.read_csv(in_dir + 'solutions.csv')
    solutions = solutions.assign(_time=np.nan, _qual=0, _error=np.nan)
    for idx, row in solutions.iterrows():
        if seed is None:
            file = '{}_{}_{}.trace'.format(out_dir + row['Instance'], alg_name, timeout)
        else:
            file = '{}_{}_{}_{}.trace'.format(out_dir + row['Instance'], alg_name, timeout, seed)
        with open(file) as f:
            for line in f:
                pass
            last_line = line.strip()
            _time, _qual = last_line.split(', ')
            solutions.loc[idx, '_time'] = float(_time)
            solutions.loc[idx, '_qual'] = int(_qual)
            solutions.loc[idx, '_error'] = (int(_qual) - row['Value']) / row['Value']
    return solutions


def _output_table(output_file: str, table: pd.DataFrame) -> None:
    with open(output_file, 'w') as f:
        f.write(table.to_latex(index=False,
                               header=['Dataset', 'Optimal solution', 'Running time',
                                       'Solution quality', 'Relative error'],
                               formatters={'_time': '{:0.2f}'.format,
                                           '_qual': '{:0.0f}'.format,
                                           '_error': '{:0.4f}'.format},
                               column_format='lllll'))


def table_out(in_dir: str, out_dir: str, alg: list, run: bool) -> None:
    if 'bnb' in alg:
        _check_run(in_dir=in_dir, out_dir=out_dir, alg_name='BnB', timeout=600, run=run, seed=None)
        solutions = _get_result(in_dir=in_dir, out_dir=out_dir, alg_name='BnB', timeout=600, seed=None)
        output_file = out_dir + 'bnb_table.tex'
        _output_table(output_file, solutions)

    if 'approx' in alg:
        _check_run(in_dir=in_dir, out_dir=out_dir, alg_name='Approx', timeout=1, run=run, seed=None)
        solutions = _get_result(in_dir=in_dir, out_dir=out_dir, alg_name='Approx', timeout=1, seed=None)
        output_file = out_dir + 'approx_table.tex'
        _output_table(output_file, solutions)

    if 'ls1' in alg:
        for seed in ls_seed_list:
            _check_run(in_dir=in_dir, out_dir=out_dir, alg_name='LS1', timeout=ls_timeout, run=run, seed=seed)
        solutions = pd.read_csv(in_dir + 'solutions.csv')
        solutions = solutions.assign(_time=0.0, _qual=0.0, _error=0.0)
        for seed in ls_seed_list:
            _solutions = _get_result(in_dir=in_dir, out_dir=out_dir, alg_name='LS1', timeout=ls_timeout, seed=seed)
            solutions['_time'] += _solutions['_time']
            solutions['_qual'] += _solutions['_qual']
            solutions['_error'] += _solutions['_error']
        solutions['_time'] /= len(ls_seed_list)
        solutions['_qual'] /= len(ls_seed_list)
        solutions['_error'] /= len(ls_seed_list)
        output_file = out_dir + 'ls1_table.tex'
        _output_table(output_file, solutions)
    if 'ls2' in alg:
        for seed in ls_seed_list:
            _check_run(in_dir=in_dir, out_dir=out_dir, alg_name='LS2', timeout=ls_timeout, run=run, seed=seed)
        solutions = pd.read_csv(in_dir + 'solutions.csv')
        solutions = solutions.assign(_time=0.0, _qual=0.0, _error=0.0)
        for seed in ls_seed_list:
            _solutions = _get_result(in_dir=in_dir, out_dir=out_dir, alg_name='LS2', timeout=ls_timeout, seed=seed)
            solutions['_time'] += _solutions['_time']
            solutions['_qual'] += _solutions['_qual']
            solutions['_error'] += _solutions['_error']
        solutions['_time'] /= len(ls_seed_list)
        solutions['_qual'] /= len(ls_seed_list)
        solutions['_error'] /= len(ls_seed_list)
        output_file = out_dir + 'ls2_table.tex'
        _output_table(output_file, solutions)
