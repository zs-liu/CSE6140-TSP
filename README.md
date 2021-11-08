# CSE6140-TSP
Gatech CSE6140/CX4140 Fall 2021 TSP Project
## Code structure

- `tsp_main.py`: program entry, run it with 

```console
python3 tsp_main.py -inst <filename> -alg [BnB | Approx | LS1 | LS2] -time <cutoff_in_seconds> [-seed <random_seed>]
```

- `graph.py`: load graph from datasets
- `bnb.py`: solve TSP with Branch-and-Bound
- `approx.py`: solve TSP with MST-APPROX
- `ls1.py`: solve TSP with ???
- `ls2.py`: solve TSP with ???