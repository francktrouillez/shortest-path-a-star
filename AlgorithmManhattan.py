from matplotlib.pyplot import hist
from FileHandler import FileHandler
from View import View
import heapq


class Algorithm:

    COLOR_NEIGHBOURED = "#85fc23"
    COLOR_EXPLORED = "#65d6d2"
    COLOR_SRC = "green"
    COLOR_DST = "red"
    COLOR_PATH = "#ffb700"
    COLOR_BIDIRECTIONAL = "#a834eb"


    def __init__(self, dataset, is_bidirectional):
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
        self.cost = 0
        self.iteration = 0

        if(not is_bidirectional):
            self.solve()
        else:
            self.solve_bidirectional()

        self.view = View(self, label_edges=True, speed=500)

    def get_remaining_counter(self):
        return len(self.history) - self.counter_history + 1

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
        if (self.done):
            return True
        if (self.counter_history >= len(self.history)):
            for i in range(len(self.path)-2):
                src = self.path[i]
                dst = self.path[i+1]
                self.set_edge_color(src, dst, self.COLOR_PATH)
                self.set_node_color(dst,  self.COLOR_PATH)
            self.set_edge_color(self.path[len(self.path)-2], self.path[len(self.path)-1],  self.COLOR_PATH)
            return False
        current_history = self.history[self.counter_history]
        if (current_history[0]): #edges animation
            current_history = current_history[1]
            self.iteration += 1
            for e in current_history:
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
                self.cost = g_scores[current[1]]
                print("Cost of best path : "+str(self.cost))
                break
            edge_history = []
            vertex_history = []
            if (current[1] != start and current[1] != goal):
                vertex_history.append((current[1], self.COLOR_EXPLORED))
            neighbour = self.get_neighbors(current[1])
            for n in neighbour[0]:
                edge = self.get_edge(current[1], n)
                g = g_scores[current[1]] + edge[2] #weight
                f = g + self.heuristic(n, goal)
                if n not in g_scores or g < g_scores[n]:
                    heapq.heappush(q, (f, n, current[2] + [n]))
                    edge_history.append(((current[1], n), self.COLOR_EXPLORED))
                    if (n != goal):
                        vertex_history.append((n, self.COLOR_NEIGHBOURED))
                    else:
                        self.path = current[2] + [n] 
                        self.cost = g
                        print("Cost of best path : "+str(self.cost))
                        self.history.append((True, edge_history))
                        self.history.append((False, vertex_history))
                        return
                    g_scores[n] = g
            self.history.append((True, edge_history))
            self.history.append((False, vertex_history))
        if (len(self.path) == 0) :
            print("No solution")
        else:
            print("Solution found")


    def solve_bidirectional(self):
        start = 0
        goal = 1
        q1 = [(0, start, [start])]
        q2 = [(0, goal, [goal])]
        heapq.heapify(q1)
        heapq.heapify(q2)


        self.history = []

        self.path = []

        g_scores_1 = {start: 0}
        g_scores_2 = {goal: 0}
        save_path_1 = {start : []}
        save_path_2 = {goal : []}


        isFirst = True
        q = q1

        while len(q) != 0:
            if (isFirst):
                q = q1
                g_scores = g_scores_1
                g_scores_other = g_scores_2
                save_path = save_path_1
                save_path_other = save_path_2
                toReach = goal
            else:
                q = q2
                g_scores = g_scores_2
                g_scores_other = g_scores_1
                save_path = save_path_2
                save_path_other = save_path_1
                toReach = start
            current = heapq.heappop(q)
            if current[1] == toReach:
                save_path_other[current[1]].reverse()
                self.path = current[2] + save_path_other[current[1]]
                self.cost = g_scores[current[1]] + g_scores_other[current[1]]
                print("Cost of best path : "+str(self.cost))
                break
            edge_history = []
            vertex_history = []
            if (current[1] != start and current[1] != goal):
                vertex_history.append((current[1], self.COLOR_EXPLORED))
            neighbour = self.get_neighbors(current[1])
            for n in neighbour[0]:
                edge = self.get_edge(current[1], n)
                g = g_scores[current[1]] + edge[2] #weight
                f = g + self.heuristic(n, goal)
                if n not in g_scores or g < g_scores[n]:
                    save_path[n] = current[2] + [n]
                    heapq.heappush(q, (f, n, current[2] + [n]))
                    edge_history.append(((current[1], n), self.COLOR_EXPLORED))
                    
                    g_scores[n] = g
                    if (n in save_path_other):
                        save_path_other[n].reverse()
                        self.path = current[2] + save_path_other[n]
                        self.cost = g_scores[n] + g_scores_other[n]
                        vertex_history.append((n, self.COLOR_BIDIRECTIONAL))
                        print("Cost of best path : "+str(self.cost))
                        self.history.append((True, edge_history))
                        self.history.append((False, vertex_history))
                        print("Solution found")
                        return
                    if (n != toReach):
                        vertex_history.append((n, self.COLOR_NEIGHBOURED))
            self.history.append((True, edge_history))
            self.history.append((False, vertex_history))
            isFirst = not isFirst
        if (len(self.path) == 0) :
            print("No solution")
        else :
            print("Solution found")

    def heuristic(self, a, b):
        node_a = self.get_vertex(a)
        node_b = self.get_vertex(b)
        #Compute heuristic


        return abs(node_a[0] - node_b[0]) + abs(node_a[1] - node_b[1])

