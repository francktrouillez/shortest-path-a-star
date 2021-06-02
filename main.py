from AlgorithmEuclidian import AlgorithmEuclidian
from AlgorithmChebyshev import AlgorithmChebyshev
from AlgorithmMean import AlgorithmMean
from Dijkstra import Dijkstra


if __name__ == "__main__":

    input_file = "datasets/8439_nodes.txt"

    algorithm = AlgorithmEuclidian(input_file, False)

    algorithm = AlgorithmChebyshev(input_file, False)

    algorithm = AlgorithmMean(input_file, False)

    dijkstra = Dijkstra(input_file)

