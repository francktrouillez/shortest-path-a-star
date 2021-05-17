import math

class FileHandler:
    def __init__(self, file_name):
        self.file_name = file_name

    """
    Input file format:
        nb_of_vertices
        vertice posx posy
        vertice_src vertice_dest
        ...
        node ID of the starting node = 0
        node ID of the destination node = 1
    """
    def read(self):
        E = 0
        V = 0
        edges = []
        edge_index = {}
        neighbors = {}
        vertices = {}
        n_vertices = -1
        with open(self.file_name, "r") as f:
            for line in f.readlines():
                element = line.split()
                if n_vertices == -1:
                    n_vertices = int(element[0])
                    V = n_vertices
                elif n_vertices != 0:
                    vertices[int(element[0])] = (int(element[1]), int(element[2]))
                    n_vertices -= 1
                elif n_vertices == 0:
                    v1 = int(element[0])
                    v2 = int(element[1])
                    w = round(math.sqrt((vertices[v2][1] - vertices[v1][1])**2 + (vertices[v2][0] - vertices[v1][0])**2), 2)
                    edges.append((v1, v2, w, "black"))
                    edge_index[(v1, v2)] = E

                    if v1 == 0:
                        neighbors.setdefault(v1, ([], "green"))[0].append(v2)
                    elif v1 == 1:
                        neighbors.setdefault(v1, ([], "red"))[0].append(v2)
                    else:
                        neighbors.setdefault(v1, ([], "grey"))[0].append(v2)

                    if v2 == 0:
                        neighbors.setdefault(v2, ([], "green"))[0].append(v1)
                    elif v2 == 1:
                        neighbors.setdefault(v2, ([], "red"))[0].append(v1)
                    else:
                        neighbors.setdefault(v2, ([], "grey"))[0].append(v1)

                    E += 1
        return E, V, vertices, edges, edge_index, neighbors

    def write(self, file):
        string = ""
        for i in range(200):
            for j in range(4):
                string += str(i)

                string += " "
                string += str(i + j + 1)
                string += " "
                string += str(12)
                string += "\n"
        f = open(file, "a")
        f.write(string)
        f.close()
