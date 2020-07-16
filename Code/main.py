from tkinter import *
from graph import load_graph_list, embed_graph_list
import networkx as nx
from canonical_ordering import get_canonical_ordering
from shilft_algorithm import shift_algorithm
from triangulation import triangulate_embedding

PAD = 10


class App:
    def __init__(self):
        self.window = Tk()
        # self.window.geometry("{0}x{1}+0+0".format(
        #    self.window.winfo_screenwidth() - PAD, self.window.winfo_screenheight() - PAD))
        self.window.title("Planar graph drawing on a grid")

        self.grid = None

        self.graph_list = embed_graph_list(load_graph_list("graph_lst.lst"))
        self.current_graph_index = -1

        self.button = Button(self.window, text="Set window full screen and then click me", command=self.init_canvas)
        self.button.pack()

    def init_canvas(self):
        self.window.update()
        self.grid = GridCanvas(self.window,
                               self.window.winfo_width(),
                               self.window.winfo_height() - self.button.winfo_height())
        self.grid.pack()
        self.button.configure(text="Change graph", command=self.change_graph)

    def change_graph(self):
        self.current_graph_index += 1
        if self.current_graph_index >= len(self.graph_list):
            self.current_graph_index = 0
        embedding = self.graph_list[self.current_graph_index]

        embedding_t, external_face = triangulate_embedding(embedding)
        ordering = get_canonical_ordering(embedding_t, external_face)
        x_pos, y_pos = shift_algorithm(ordering)

        # x_pos, y_pos = shift_algorithm.run()

        self.grid.draw_graph(embedding, x_pos, y_pos)
        # self.grid.draw_graph(embedding_t, x_pos, y_pos)
        self.window.update()

    def run(self):
        self.window.mainloop()


class GridCanvas(Canvas):
    def __init__(self, parent, container_width, container_height):
        self.n = 0
        self.width = 0
        self.height = 0
        self.cell_size = 0
        self.pad_x = PAD
        self.pad_y = PAD
        self.container_width = container_width
        self.container_height = container_height - 5
        Canvas.__init__(self,
                        parent,
                        width=container_width,
                        height=container_height)
        self.create_line(100, 0, 100, container_height)
        # def update_container_size(self, container_width, container_height):
        #     self.master_width = container_width

    def set_n(self, n):
        self.n = n
        self.width = 2 * self.n - 4
        self.height = self.n - 2
        self.update_cell_size()

    def update_cell_size(self):
        cell_x = (self.container_width - 2*PAD) / (2*self.n - 4)
        cell_y = (self.container_height - 2*PAD) / (self.n - 2)
        if cell_x > cell_y:  # if the cell size is constrained by the height of the window
            self.cell_size = cell_y
            self.pad_y = PAD
            self.pad_x = (self.container_width - ((2*self.n-4)*self.cell_size))/2
        else:  # if the cell size is constrained by the width of the window
            self.cell_size = cell_x
            self.pad_x = PAD
            self.pad_y = (self.container_height - ((self.n-2)*self.cell_size))/2

    def display_borders(self):
        h = self.pad_y + self.height * self.cell_size
        w = self.pad_x + self.width * self.cell_size

        self.create_line(1, 1, 1, h, fill='red')
        self.create_line(1, 1, w, 1, fill='green')
        self.create_line(1, h, w, h, fill='blue')
        self.create_line(w, h, w, 1, fill='yellow')

    def draw_grid(self):
        for i in range(self.width):
            for j in range(self.height):
                self.draw_point(i, j)

    def draw_point(self, x, y):
        x_window, y_window = self.to_grid_coordinates(x, y)
        # self.create_oval(x_window, y_window, x_window, y_window, width=0, fill='red')
        self.create_line(x_window, y_window, x_window + 1, y_window)

    def draw_edge(self, x1, y1, x2, y2, color):
        x1_window, y1_window = self.to_grid_coordinates(x1, y1)
        x2_window, y2_window = self.to_grid_coordinates(x2, y2)
        self.create_line(x1_window, y1_window, x2_window, y2_window, fill=color)

    def to_grid_coordinates(self, x, y):
        return self.pad_x + x * self.cell_size, self.container_height - (self.pad_y + y * self.cell_size)

    def add_text(self, txt, x, y):
        x_window, y_window = self.to_grid_coordinates(x, y)
        self.create_text(x_window, y_window, text=txt)

    def draw_graph(self, g: nx.PlanarEmbedding, x_coord, y_coord):
        self.delete("all")
        self.set_n(len(g))
        # self.display_borders()
        self.draw_grid()
        for i in range(len(g)):
            self.add_text(str(i+1), x_coord[i], y_coord[i])
            for n in g.neighbors(i):
                if n > i:
                    # if g.is_dummy_edge(i, n):
                    self.draw_edge(x_coord[i], y_coord[i], x_coord[n], y_coord[n], 'green')
                    # else:
                    #    self.draw_edge(x_coord[i], y_coord[i], x_coord[n], y_coord[n], 'red')


if __name__ == "__main__":
    app = App()
    """
    G = load_graph1()
    dfs = DFS(G)
    print(dfs.get_ordering())
    """

    """
    print("-------")

    for i in range(len(g)):
        print(G.neighbors(i))

    print("-------")
    """
    app.run()
