import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.widgets as widgets
import time
import threading
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
        self.is_playing = False
        self.is_thread_alive = False
        self.init_graph()
        self.init_buttons()
        self.init_labels()
        plt.show()


    def init_labels(self):
        if (self.algorithm.get_iteration() != 0):
            text_iteration = "Iteration : "+str(self.algorithm.get_iteration())
        else:
            text_iteration = ""
        self.iterations_label = plt.text(-5,0.2, text_iteration)
        if (self.is_playing):
            self.state_run = plt.text(-2,0.2, "Playing")
        else:
            self.state_run = plt.text(-2,0.2, "Paused")

    def init_graph(self):
        self.ax.clear()
        plt.clf()
        plt.cla()
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
        

    def init_buttons(self):
        def animate():
            self.algorithm.update()
            self.ax.clear()
            plt.clf()
            plt.cla()
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
            self.init_buttons()
            self.init_labels()
            
        def playThread():
            time.sleep(self.speed/1000)
            while(self.is_playing and self.algorithm.get_remaining_counter() > 0):
                animate()
                plt.draw()
                time.sleep(self.speed/1000)
            self.is_thread_alive = False
            self.is_playing = False
        
        def play(event):
            if (self.is_thread_alive):
                return
            self.is_playing = True
            self.is_thread_alive = True
            thread = threading.Thread(target = playThread)
            thread.start()

        def pause(event):
            self.is_playing = False
            self.state_run.set_text("Paused")
            plt.show()
        def next(event):
            animate()
            plt.show()
        
        self.button_play = widgets.Button(plt.axes([0.8,0,0.1,0.05]), "Play")
        self.button_pause = widgets.Button(plt.axes([0.9,0,0.1,0.05]), "Pause")
        self.button_next = widgets.Button(plt.axes([0.7,0,0.1,0.05]), "Next")

        self.button_play.on_clicked(play)
        self.button_pause.on_clicked(pause)
        self.button_next.on_clicked(next)

