from FileHandler import FileHandler
from View import View


class Algorithm:

    def __init__(self, dataset):
        fh = FileHandler(dataset)
        self.E, self.V, self.vertices, self.edges, self.edge_index, self.nodes = fh.read()
        # E is total number of edges
        # V is total number of vertices
        # vertices is a dictionary that contain vertex id as key and a tuple (position x, position y) as value
        # edges is a list of tuples (source, destination, weight, color)
        # nodes is a dictionary that stores the index of each edges in the list above
        # nodes is a dictionary where we can get direct neighbors of each nodes and the color assigned to each node

        self.finish = False
        self.saved = False

        # if you want to solve before visualizing the process you can do it here, or you can solve during the
        # visualization in the update function

        # you can delete this it is for the example presented in the update function below
        self.color = ["blue", "red", "green", "m"]
        self.counter = 0

        self.view = View(self, label_edges=True, speed=20)

    def get_edges(self):
        return self.edges

    def set_edge_color(self, src, dest, color):
        if (src, dest) in self.edge_index:
            index = self.edge_index[(src, dest)]
            self.edges[index] = self.edges[index][0], self.edges[index][1], self.edges[index][2], color
        elif (dest, src) in self.edge_index:
            index = self.edge_index[(dest, src)]
            self.edges[index] = self.edges[index][0], self.edges[index][1], self.edges[index][2], color

    def get_neighbors(self, v):
        return self.nodes[v]

    def get_vertices(self):
        return self.vertices

    def get_finish(self):
        return self.finish

    def save(self):
        self.saved = True
        self.finish = False

    def update(self):
        """
        updated constantly during each refresh of the view
        :return: void
        """

        # example where one edge is changing color every tick
        self.set_edge_color(16, 19, self.color[self.counter % 4])
        self.counter += 1


algorithm = Algorithm("datasets/example")
