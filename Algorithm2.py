from matplotlib.pyplot import hist
from FileHandler import FileHandler
from View import View
import heapq


class Algorithm:

    COLOR_EXPLORED = "#65d6d2"
    COLOR_SRC = "green"
    COLOR_DST = "red"
    COLOR_PATH = "#ffb700"


    def __init__(self, dataset):
        fh = FileHandler(dataset)
        self.E, self.V, self.vertices, self.edges, self.edge_index, self.nodes = fh.read()
        # E is total number of edges
        # V is total number of vertices
        # vertices is a dictionary that contain vertex id as key and a tuple (position x, position y) as value
        # edges is a list of tuples (source, destination, weight, color)
        # edge_index is a dictionary that stores the index of each edges in the list above
        # nodes is a dictionary where we can get direct neighbors of each nodes and the color assigned to each node

        self.finish = False
        self.saved = False

        # if you want to solve before visualizing the process you can do it here, or you can solve during the
        # visualization in the update function
        self.counter_history = 0
        self.history = []
        self.path = []
        self.done = False

        self.solve()

        print("Solution found")


        self.view = View(self, label_edges=True, speed=500)

    def get_edges(self):
        return self.edges

    def set_edge_color(self, src, dest, color):
        if (src, dest) in self.edge_index:
            index = self.edge_index[(src, dest)]
            self.edges[index] = self.edges[index][0], self.edges[index][1], self.edges[index][2], color
        elif (dest, src) in self.edge_index:
            index = self.edge_index[(dest, src)]
            self.edges[index] = self.edges[index][0], self.edges[index][1], self.edges[index][2], color

    def set_node_color(self, node_id, color):
        self.nodes[node_id] = (self.nodes[node_id][0], color)

    def get_edge(self, a, b):
        if (a, b) in self.edge_index:
            index = self.edge_index[(a, b)]
            return self.edges[index]
        elif (b, a) in self.edge_index:
            index = self.edge_index[(b, a)]
            return self.edges[index]

    def get_neighbors(self, v):
        return self.nodes[v]

    def get_vertices(self):
        return self.vertices

    def get_finish(self):
        return self.finish

    def get_vertex(self, id):
        return self.vertices[id]

    def save(self):
        self.saved = True
        self.finish = False

    def update(self):
        """
        updated constantly during each refresh of the view
        :return: void
        """
        if (self.done):
            return True
        if (self.counter_history >= len(self.history)):
            for i in range(len(self.path)-2):
                src = self.path[i]
                dst = self.path[i+1]
                self.set_edge_color(src, dst, self.COLOR_PATH)
                self.set_node_color(dst,  self.COLOR_PATH)
            self.set_edge_color(self.path[len(self.path)-2], 1,  self.COLOR_PATH)
            return False
        current_history = self.history[self.counter_history]
        if (current_history[0]): #edges animation
            current_history = current_history[1]
            for e in current_history:
                print(e)
                self.set_edge_color(e[0][0], e[0][1], e[1])
        else: #Vertex animation
            current_history = current_history[1]
            for n in current_history:
                self.set_node_color(n[0], n[1])

        self.counter_history +=1
        return False

    def solve(self):
        start = 0
        goal = 1
        q = [(0, start, [start])]
        heapq.heapify(q)

        self.history = []

        self.path = []

        g_scores = {start: 0}
        while len(q) != 0:
            current = heapq.heappop(q)
            if current[1] == goal:
                self.path = current[2]
                break
            edge_history = []
            vertex_history = []
            neighbour = self.get_neighbors(current[1])
            for n in neighbour[0]:
                edge = self.get_edge(current[1], n)
                g = g_scores[current[1]] + edge[2] #weight
                f = g + self.heuristic(n, goal)
                if n not in g_scores or g < g_scores[n]:
                    heapq.heappush(q, (f, n, current[2] + [n]))
                    edge_history.append(((current[1], n), self.COLOR_EXPLORED))
                    if (n != goal):
                        vertex_history.append((n, self.COLOR_EXPLORED))
                    g_scores[n] = g
            self.history.append((True, edge_history))
            self.history.append((False, vertex_history))

    def heuristic(self, a, b):
        node_a = self.get_vertex(a)
        node_b = self.get_vertex(b)
        #Compute heuristic


        return abs(node_a[0] - node_b[0]) + abs(node_a[1] - node_b[1])
