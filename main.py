from AlgorithmEuclidean import AlgorithmEuclidean
from AlgorithmChebyshev import AlgorithmChebyshev
from AlgorithmMean import AlgorithmMean
from Dijkstra import Dijkstra


if __name__ == "__main__":

    input_file = "datasets/8439_nodes.txt"

    #algorithm = AlgorithmEuclidean(input_file, False)

    #algorithm = AlgorithmEuclidean(input_file, True)


    algorithm = AlgorithmEuclidean(input_file, True, True)


    #algorithm = AlgorithmChebyshev(input_file, False)

    #algorithm = AlgorithmMean(input_file, False)

    #dijkstra = Dijkstra(input_file)

