from typing import List
import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.widgets import Button, CheckButtons, TextBox
from shift_algorithm import compute_pos, triangulate_embedding


# If the size of the graph is grander than this constant, the vertices will not be annotated.
MAX_SIZE_ANNOTATION = 50


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
        self.x_pos = None
        self.y_pos = None

        self.display_dummy_edges = True

    def change_graph(self, hop: int = 1):
        old_index = self.current_graph_index
        self.current_graph_index += hop
        if self.current_graph_index >= len(self.graph_list):
            self.current_graph_index -= len(self.graph_list)
        elif self.current_graph_index < 0:
            self.current_graph_index += len(self.graph_list)
        if old_index != self.current_graph_index:
            self.current_graph = self.graph_list[self.current_graph_index]
            self.embedding_t, _ = triangulate_embedding(self.current_graph)
            self.x_pos, self.y_pos = compute_pos(self.current_graph)
            self.update_display()

    def update_display(self):
        pass

    def draw_graph(self):
        g = self.current_graph
        for i in range(len(g)):
            if len(g) < MAX_SIZE_ANNOTATION:
                self.add_text(i)
            for n in self.embedding_t.neighbors(i):
                if n > i:
                    if g.has_edge(i, n):
                        self.draw_edge(i, n, 'black')
                    elif self.display_dummy_edges:
                        self.draw_edge(i, n, 'green')

    def draw_edge(self, u, v, color):
        draw_edge(self.x_pos[u], self.y_pos[u], self.x_pos[v], self.y_pos[v], color)

    def add_text(self, v):
        add_text(str(v+1), self.x_pos[v], self.y_pos[v])


class AppMatplotlib(App):
    def __init__(self, graph_list: List[nx.PlanarEmbedding]):
        App.__init__(self, graph_list)

        self.fig, self.ax = plt.subplots()
        self.fig.canvas.set_window_title('Planar graph drawing on a grid')
        plt.subplots_adjust(left=0, right=1, top=1, bottom=0)

        self.prev_button = None
        self.next_button = None
        self.check_button = None

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
        axckeckbox = plt.axes([0.01, 0.81, 0.1, 0.1], frameon=False)
        self.check_button = CheckButtons(axckeckbox, ["Dummy edges"], [self.display_dummy_edges])
        self.check_button.on_clicked(self.toggle_dummy_edges)
        axes_text_box = plt.axes([0.01, 0.76, 0.06, 0.075], frameon=False)
        text_box = TextBox(axes_text_box, "", "Nodes : " + str(len(self.current_graph)))

    def toggle_dummy_edges(self, event=None):
        self.display_dummy_edges = not self.display_dummy_edges
        self.update_display()

    def update_display(self):
        self.fig.clear()
        self.draw_graph()
        plt.axis('equal')
        # plt.gca().set_aspect('equal', adjustable='box')
        # plt.axis('off')
        # plt.grid()
        self.add_widgets()
