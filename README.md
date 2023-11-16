# Shortest path algorithms with A*

This project has been conducted as part of the course "INFO-H410 - Techniques of artificial intelligence" at the Ecole Polytechnique de Bruxelles - ULB, given from September 2020 and January 2021. The contributors are Alexandre Missenard, Andrey Sobolevsky and Franck Trouillez.

## How to run

In order to run the project, you need to install `networkx`:

```bash
pip install networkx
```


Then, simply run the `main` file.

```bash
python main.py
```

## Description

This project aims at implement A* algorithms for the shortest path problem in a nodes graph.

3 different heuristics are implemented:
- Mean distance
- Chebyshev distance
- Euclidean distance

For each heuristic, the algorithm is run with a unidirectional search, and a bidirectional search, which is a new way to implement A*. The bidirectional search is implemented in order to allow parallelization of the searches. However, even if the solution is found faster, it doesn't ensure its optimality anymore.

The algorithm is tested on different instances generated ourselves. The instances are generated with a random number of nodes, and a random number of edges. The edges are generated with a random weight, and a random direction.

![description](/images/description.png)

## Architecture

The A* algorithm is implemented in `Algorithm`.

3 sub-classes are created to define the heuristics.

The Dijkstra's algorithm is also implemented, in order to compare with A*. It is done in `Dijkstra`.

The instances can be found in the directory `datasets`. In order to read these instances, a class `FileHandler` is created, and allows to read the info in the file.

The algorithm class `Algorithm` can also use a bidirectional search, instead of the classical unidirectional search.

In order to generate the instances, an instance generator has been created, which can be found in `InstanceGenerator`.

