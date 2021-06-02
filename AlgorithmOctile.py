from math import sqrt
from Algorithm import Algorithm


class AlgorithmOctile(Algorithm):

    CONSTANT_OCTILE = sqrt(2) - 2

    def heuristic(self, a, b):
        node_a = self.get_vertex(a)
        node_b = self.get_vertex(b)
        dx = abs(node_a[0] - node_b[0])
        dy = abs(node_a[1] - node_b[1])
        #Compute heuristic


        return (dx + dy) + (sqrt(2) - 2) * min(dx, dy)
        
        #return (dx + dy) + self.CONSTANT_OCTILE * min(dx, dy)

