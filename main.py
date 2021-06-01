from AlgorithmManhattan import AlgorithmManhattan
from AlgorithmEuclidian import AlgorithmEuclidian
from AlgorithmChebyshev import AlgorithmChebyshev
from AlgorithmOctile import AlgorithmOctile
from Dijkstra import Dijkstra


if __name__ == "__main__":

    algorithm = AlgorithmEuclidian("datasets/1118_nodes.txt", False)

    algorithm = AlgorithmEuclidian("datasets/1118_nodes.txt", True, False)

    algorithm = AlgorithmEuclidian("datasets/1118_nodes.txt", True, True)



    dijkstra = Dijkstra("datasets/1118_nodes.txt")

