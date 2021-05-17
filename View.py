import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.animation as animation
# from pyvis.network import Network


class View:
    def __init__(self, algorithm, label_edges=True, speed=1000):
        self.algorithm = algorithm
        self.label_edges = label_edges
        self.speed = speed
        self.fig, self.ax = plt.subplots()
        self.G = nx.Graph()
        for v in range(len(self.algorithm.get_vertices())):
            self.G.add_node(v, pos=self.algorithm.get_vertices()[v])
        for e in self.algorithm.get_edges():
            self.G.add_edge(e[0], e[1], color=e[3], weight=e[2])
        self.pos = nx.spring_layout(self.G, pos=self.algorithm.get_vertices(), fixed=self.algorithm.get_vertices())
        self.run_animation()

    def run_animation(self):
        def animate(i):
            self.ax.clear()
            plt.clf()
            plt.cla()
            self.algorithm.update()
            for v in range(len(self.algorithm.get_vertices())):
                self.G.add_node(v, pos=self.algorithm.get_vertices()[v])
            for e in self.algorithm.get_edges():
                self.G.add_edge(e[0], e[1], color=e[3], weight=e[2])
            edge_colors = [self.G[u][v]['color'] for u, v in self.G.edges()]
            node_colors = []
            counter = 0
            for node in self.G:
                node_colors.append(self.algorithm.get_neighbors(counter)[1])
                counter += 1
            nx.draw(self.G, nx.get_node_attributes(self.G, 'pos'), with_labels=True, node_color=node_colors,
                    node_size=500, width=3, edge_color=edge_colors)
            if self.label_edges:
                edge_labels = dict([((u, v,), d['weight'])
                                    for u, v, d in self.G.edges(data=True)])
                nx.draw_networkx_edge_labels(self.G, self.pos, edge_labels=edge_labels, font_size=6)

        ani = animation.FuncAnimation(self.fig, animate, interval=self.speed, blit=False)
        plt.show()
