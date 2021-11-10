import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from evaluate import _check_run

ls_timeout = 600
ls_seed_list = list(range(0, 1))
q_list = [x / 100 for x in [0.0, 0.1, 0.2, 0.5, 1.0]]

instances = ['Atlanta', 'SanFrancisco']


def qrtd_out(in_dir: str, out_dir: str, alg: list, run: bool):
    solutions = pd.read_csv(in_dir + 'solutions.csv')
    for _alg in alg:
        for instance in instances:
            time_qual_list = []
            solution = solutions.loc[solutions['Instance'] == instance, 'Value'].values[0]
            for seed in ls_seed_list:
                _check_run(in_dir=in_dir, out_dir=out_dir, alg_name=_alg.upper(), timeout=ls_timeout, run=run,
                           seed=seed, instances=[instance])
                file = '{}_{}_{}_{}.trace'.format(out_dir + instance, _alg.upper(), ls_timeout, seed)
                time_qual_list.append(pd.read_csv(file, names=['_time', '_qual']))
            time_qual = pd.concat(time_qual_list, ignore_index=True)
            time_qual = time_qual.assign(rel_qual=(time_qual['_qual'] - solution) / solution)
            time_qual = time_qual.sort_values('_time')

            fig, ax = plt.subplots(nrows=1, ncols=1, dpi=150)
            ax.set_xlabel("Running time", fontweight="bold")
            ax.set_ylabel("Percent", fontweight="bold")
            for q in q_list:
                mask = time_qual[time_qual['rel_qual'] <= q]
                ax.step([0.0] + list(mask['_time'].array), np.arange(0, mask.shape[0] + 1) / time_qual.shape[0],
                        label=u'q={:0.0f}‰'.format(q * 1000))
            ax.legend(loc='best')
            fig_file = out_dir + _alg + instance.lower() + '.pdf'
            fig.savefig(fig_file)
            plt.close(fig)
