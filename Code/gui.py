from typing import List
import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.widgets import Button, CheckButtons, TextBox

from canonical_ordering import get_canonical_ordering
from shift_algorithm import triangulate_embedding, shift_algorithm


def draw_edge(x1, y1, x2, y2, c: str):
    plt.plot((x1, x2), (y1, y2), color=c, linewidth=.5)


def add_text(txt, x, y):
    plt.annotate(txt, xy=(x, y))


class App:
    def __init__(self, graph_list: List[nx.PlanarEmbedding]):
        self.graph_list = graph_list
        self.current_graph_index = -1
        self.current_graph = None
        self.embedding_t = None
        self.ordering = None
        self.x_pos = None
        self.y_pos = None

        self.display_dummy_edges = True
        self.display_can_order = False

    def change_graph(self, hop: int = 1):
        old_index = self.current_graph_index
        self.current_graph_index += hop
        if self.current_graph_index >= len(self.graph_list):
            self.current_graph_index -= len(self.graph_list)
        elif self.current_graph_index < 0:
            self.current_graph_index += len(self.graph_list)
        if old_index != self.current_graph_index:
            self.current_graph = self.graph_list[self.current_graph_index]
            self.embedding_t, external_face = triangulate_embedding(self.current_graph)
            self.ordering, wpq_list = get_canonical_ordering(self.embedding_t, external_face)
            self.x_pos, self.y_pos = shift_algorithm(self.ordering, wpq_list)
            self.update_display()

    def update_display(self):
        raise NotImplementedError()

    def draw_graph(self):
        g = self.current_graph
        if self.display_can_order:
            for i, v in enumerate(self.ordering):
                self.add_text(v, i)
        for i in range(len(g)):
            for n in self.embedding_t.neighbors(i):
                if n > i:
                    if g.has_edge(i, n):
                        self.draw_edge(i, n, 'black')
                    elif self.display_dummy_edges:
                        self.draw_edge(i, n, 'green')

    def draw_edge(self, u, v, color):
        draw_edge(self.x_pos[u], self.y_pos[u], self.x_pos[v], self.y_pos[v], color)

    def add_text(self, v, index):
        add_text(index, self.x_pos[v], self.y_pos[v])


class AppMatplotlib(App):
    def __init__(self, graph_list: List[nx.PlanarEmbedding]):
        App.__init__(self, graph_list)

        self.fig, self.ax = plt.subplots()
        self.fig.canvas.set_window_title('Planar graph drawing on a grid')
        plt.subplots_adjust(left=0, right=1, top=1, bottom=0)

        self.display_can_order = True
        self.prev_button = None
        self.next_button = None
        self.dummy_edge_button = None
        self.can_order_button = None

        self.change_graph()

        plt.show()
        plt.close()

    def add_widgets(self):
        axprev = plt.axes([0.01, 0.9, 0.1, 0.075])
        axnext = plt.axes([0.12, 0.9, 0.1, 0.075])
        self.prev_button = Button(axprev, "Previous")
        self.prev_button.on_clicked(lambda event: self.change_graph(-1))
        self.next_button = Button(axnext, "Next")
        self.next_button.on_clicked(lambda event: self.change_graph())
        axcanbox = plt.axes([0.01, 0.81, 0.1, 0.1], frameon=False)
        self.can_order_button = CheckButtons(axcanbox, ["Canonical order"], [self.display_can_order])
        self.can_order_button.on_clicked(self.toggle_can_order)
        axckeckbox = plt.axes([0.01, 0.76, 0.1, 0.1], frameon=False)
        self.dummy_edge_button = CheckButtons(axckeckbox, ["Dummy edges"], [self.display_dummy_edges])
        self.dummy_edge_button.on_clicked(self.toggle_dummy_edges)
        axes_text_box = plt.axes([0.01, 0.69, 0.06, 0.075], frameon=False)
        text_box = TextBox(axes_text_box, "", "Nodes : " + str(len(self.current_graph)))

    def toggle_dummy_edges(self, event=None):
        self.display_dummy_edges = not self.display_dummy_edges
        self.update_display()

    def toggle_can_order(self, event=None):
        self.display_can_order = not self.display_can_order
        self.update_display()

    def update_display(self):
        self.fig.clear()
        self.draw_graph()
        plt.axis('equal')
        # plt.gca().set_aspect('equal', adjustable='box')
        # plt.axis('off')
        self.add_widgets()
