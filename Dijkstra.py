from matplotlib.pyplot import hist
from FileHandler import FileHandler
from View import View
import sys
import time


class Dijkstra:

    COLOR_NEIGHBOURED = "#85fc23"
    COLOR_EXPLORED = "#65d6d2"
    COLOR_SRC = "green"
    COLOR_DST = "red"
    COLOR_PATH = "#ffb700"
    COLOR_BIDIRECTIONAL = "#a834eb"
    COLOR_CURRENT = "#ff9d00"

    UNDEFINED = -1



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
        self.cost = 0
        self.iteration = 0

        start = time.time()

        self.solve()

        end = time.time()
        print("Time elapsed (ms) : "+str(int((end-start)*1000*1000)/1000))

        self.remove_bad_history()

        self.view = View(self, label_edges=True, speed=500)

    def remove_bad_history(self):
        real_history = []
        for h in self.history:
            if (len(h[1]) > 0):
                real_history.append(h)
        self.history = real_history 

    def get_remaining_counter(self):
        return len(self.history) - self.counter_history + 1

    def get_length_history(self):
        return len(self.history)
    
    def get_counter_history(self):
        return self.counter_history

    def reinitialize_history(self, data):
        self.iteration = 0
        self.counter_history = 0
        edges, nodes = data
        self.edges = edges
        self.nodes = nodes
    
    def get_nodes(self):
        return self.nodes

    def get_iteration(self):
        return self.iteration

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
        if (self.counter_history > len(self.history)):
            return self.counter_history
        if (self.counter_history == len(self.history)):
            for i in range(len(self.path)-2):
                src = self.path[i]
                dst = self.path[i+1]
                self.set_edge_color(src, dst, self.COLOR_PATH)
                self.set_node_color(dst,  self.COLOR_PATH)
            self.set_edge_color(self.path[len(self.path)-2], self.path[len(self.path)-1],  self.COLOR_PATH)
            self.counter_history += 1
            return self.counter_history
        current_history = self.history[self.counter_history]
        if (current_history[0] == 0): #current
            self.iteration += 1
            current_history = current_history[1]
            if (len(current_history) == 0):
                self.counter_history += 1
                return self.update()
            for n in current_history:
                self.set_node_color(n[0], n[1])
        elif (current_history[0] == 1): #edges animation
            current_history = current_history[1]
            if (len(current_history) == 0):
                self.counter_history += 1
                return self.update()
            for e in current_history:
                self.set_edge_color(e[0][0], e[0][1], e[1])
        else: #Vertex animation
            current_history = current_history[1]
            if (len(current_history) == 0):
                self.counter_history += 1
                return self.update()
            for n in current_history:
                self.set_node_color(n[0], n[1])
            
        self.counter_history +=1
        return self.counter_history

    def get_vertex_with_minimal_distance(self, distances, remaining_nodes):
        min_node = self.UNDEFINED
        min_value = sys.maxsize
        for node in distances:
            if (node not in remaining_nodes):
                continue
            if (distances[node] < min_value):
                min_node = node
                min_value = distances[node]
        return min_node


    def solve(self):
        start = 0
        goal = 1

        distances = {}
        predecessors = {}
        set_of_vertices = set()

        for v in self.vertices:
            distances[v] = sys.maxsize
            predecessors[v] = self.UNDEFINED
            set_of_vertices.add(v)

        distances[start] = 0

        while (len(set_of_vertices) > 0):
            current = self.get_vertex_with_minimal_distance(distances, set_of_vertices)
            if (current == self.UNDEFINED):
                print("Error undefined")
                return
            if (current == goal):
                self.cost = distances[goal]
                print("Cost of best path : "+str(self.cost))
                break
            set_of_vertices.remove(current)
            edge_history = []
            vertex_history = []
            current_history = []
            if (current != start and current != goal):
                current_history.append((current, self.COLOR_CURRENT))
                vertex_history.append((current, self.COLOR_EXPLORED))
            neighbour = self.get_neighbors(current)
            for n in neighbour[0]:
                if (n not in set_of_vertices):
                    continue
                edge = self.get_edge(current, n)
                potential_distance = distances[current] + edge[2]
                if (potential_distance < distances[n]):
                    distances[n] = potential_distance
                    predecessors[n] = current
                    edge_history.append(((current, n), self.COLOR_EXPLORED))
                    if (n != goal):
                        vertex_history.append((n, self.COLOR_NEIGHBOURED))
            self.history.append((0, current_history))
            self.history.append((1, edge_history))
            self.history.append((2, vertex_history))
        
        if (predecessors[goal] == self.UNDEFINED):
            print("No solution")
        else:
            print("Solution found")
            path = []
            current = goal
            while (current != self.UNDEFINED):
                path = [current] + path
                current = predecessors[current]
            self.path = path
