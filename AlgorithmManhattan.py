from Algorithm import Algorithm


class AlgorithmManhattan(Algorithm):
    
    def heuristic(self, a, b):
        node_a = self.get_vertex(a)
        node_b = self.get_vertex(b)
        #Compute heuristic


        return abs(node_a[0] - node_b[0]) + abs(node_a[1] - node_b[1])

