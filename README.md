# CSE6140-TSP
Gatech CSE6140/CX4140 Fall 2021 TSP Project
## Code structure

- `tsp_main.py`: program entry, has four arguments
    - `-inst`: the path of the input dataset
    - `-alg`: the algorithm, from Branch-and-Bound / Approximation / Local Search 1 / Local Search 2
    - `-time`: cutoff time, in seconds
    - `-seed`: random seed
    - Usage:
        ```console
        python3 tsp_main.py -inst <filename> -alg [BnB | Approx | LS1 | LS2] -time <cutoff_in_seconds> [-seed <random_seed>]
        ```
- `eva_main.py`: evaluation entry, has five arguments
    - `-out`: the evaluation method, from Comprehensive Table / QRTDs / SQDs / Box plots
    - `-i`: the input path
    - `-o`: the output path
    - `-run`: whether force it to rerun all algorithms
    - `-alg`: the algorithm, from Branch-and-Bound / Approximation / Local Search 1 / Local Search 2 / All algorithms
    - Usage:
        ```console
        python3 eva_main.py -out [table | qrtd | sqd | box] -i <input_path> -o <output_path> -run [T | F] -alg [BnB | Approx | LS1 | LS2 | all]
        ```
- `evaluate/*`: evaluate results
- `graph.py`: load graph from datasets
- `bnb.py`: solve TSP with Branch-and-Bound
- `approx.py`: solve TSP with MST-APPROX
- `ls1.py`: solve TSP with SA
- `ls2.py`: solve TSP with ???
