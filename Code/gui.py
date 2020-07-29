from typing import List
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import networkx as nx
from load_graph import embed_graph_list, load_graph_list
from shift_algorithm import compute_pos, triangulate_embedding


def draw_edge(x1, y1, x2, y2, c: str):
    plt.plot((x1, x2), (y1, y2), color=c, linewidth=.5)


def add_text(txt, x, y):
    plt.annotate(txt, xy=(x, y))


class App:
    def __init__(self, file_paths: List[str]):

        self.fig, self.ax = plt.subplots()
        self.fig.canvas.set_window_title('Planar graph drawing on a grid')

        plt.subplots_adjust(left=0, right=1, top=1, bottom=0)

        self.graph_list = []
        for file_path in file_paths:
            self.graph_list += embed_graph_list(load_graph_list(file_path))
        # self.graph_list = [g for g in self.graph_list if len(g)>50]
        self.current_graph_index = -1
        self.current_graph = None

        self.prev_button = None
        self.next_button = None

        self.change_graph()

        plt.show()
        plt.close()

    def add_buttons(self):
        axprev = plt.axes([0.01, 0.9, 0.1, 0.075])
        axnext = plt.axes([0.12, 0.9, 0.1, 0.075])
        self.prev_button = Button(axprev, "Previous")
        self.prev_button.on_clicked(lambda event: self.change_graph(event, -1))
        self.next_button = Button(axnext, "Next")
        self.next_button.on_clicked(self.change_graph)

    def change_graph(self, event=None, hop: int = 1):
        self.current_graph_index += hop
        if self.current_graph_index >= len(self.graph_list):
            self.current_graph_index -= len(self.graph_list)
        elif self.current_graph_index < 0:
            self.current_graph_index += len(self.graph_list)
        self.current_graph = self.graph_list[self.current_graph_index]

        embedding_t, _ = triangulate_embedding(self.current_graph)
        x_pos, y_pos = compute_pos(self.current_graph)

        self.fig.clear()
        self.draw_graph(embedding_t, x_pos, y_pos)
        plt.axis('equal')
        # plt.gca().set_aspect('equal', adjustable='box')
        # plt.axis('off')
        # plt.grid()

        self.add_buttons()

    def draw_graph(self, g_triangulated: nx.PlanarEmbedding, x_coord: list, y_coord: list):
        g = self.current_graph
        for i in range(len(g)):
            add_text(str(i+1), x_coord[i], y_coord[i])
            for n in g_triangulated.neighbors(i):
                if n > i:
                    if g.has_edge(i, n):
                        draw_edge(x_coord[i], y_coord[i], x_coord[n], y_coord[n], 'black')
                    else:
                        draw_edge(x_coord[i], y_coord[i], x_coord[n], y_coord[n], 'green')
