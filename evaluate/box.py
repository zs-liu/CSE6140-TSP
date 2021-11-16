import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from evaluate import _check_run

plt.rcParams["font.family"] = "Linux Libertine O"

ls_timeout = 600
ls_seed_list = list(range(0, 2))
q_list = [x / 100 for x in [0.0, 1, 2, 5, 10.0]]

instances = ['Atlanta']


def box_out(in_dir: str, out_dir: str, alg: list, run: bool):
    solutions = pd.read_csv(in_dir + 'solutions.csv')
    for _alg in alg:
        for instance in instances:
            solution = solutions.loc[solutions['Instance'] == instance, 'Value'].values[0]
            for seed in ls_seed_list:
                _check_run(in_dir=in_dir, out_dir=out_dir, alg_name=_alg.upper(), timeout=ls_timeout, run=run,
                           seed=seed, instances=[instance])

            fig, ax = plt.subplots(nrows=1, ncols=1, dpi=150)
            ax.set_xlabel("Relative error", fontweight="bold")
            ax.set_ylabel("Running time (s)", fontweight="bold")
            time_lists = []
            label_lists = []
            for q in q_list:
                time_list = []
                for seed in ls_seed_list:
                    file = '{}_{}_{}_{}.trace'.format(out_dir + instance, _alg.upper(), ls_timeout, seed)
                    time_qual = pd.read_csv(file, names=['_time', '_qual'])
                    time_qual = time_qual.assign(rel_qual=(time_qual['_qual'] - solution) / solution)
                    time_qual = time_qual[time_qual['rel_qual'] <= q]
                    if time_qual.shape[0] != 0:
                        time_list.append(np.min(time_qual['_time']))
                if len(time_list) != 0:
                    time_lists.append(time_list)
                    label_lists.append(u'q={:0.0f}%'.format(q * 100))
            ax.boxplot(time_lists, whis=(0.0, 100.0), labels=label_lists)
            ax.legend(loc='best')
            fig_file = out_dir + _alg + instance.lower() + '_box.pdf'
            fig.savefig(fig_file)
            plt.close(fig)
