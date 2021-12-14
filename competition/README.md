# CSE6140-TSP

Gatech CSE6140/CX4140 Fall 2021 TSP Project

We only submit **Local Search** algorithm for the competition.

## Code structure

- `tsp_main.py`: program entry, has four arguments
    - `-inst`: the path of the input dataset
    - `-alg`: the algorithm, please choose this as `LS`
    - `-time`: cutoff time, in seconds
    - `-seed`: random seed
    - Usage:
        ```console
        python3 tsp_main.py -inst <filename> -alg LS -time <cutoff_in_seconds> [-seed <random_seed>]
        ```
## Random start

This local search algorithm differs from our main project submission. We add a simple random start to make full use of the running time.