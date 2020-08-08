from tkinter import *
import networkx as nx
from gui import App

PAD = 10


class AppTk(App):
    """
    Use tkinter to display graphs. The draws are less pretty than the ones generated with matplotlib (gui.py) but a lot
    faster.
    """
    def __init__(self, graph_list: nx.PlanarEmbedding):
        App.__init__(self, graph_list)

        self.window = Tk()
        self.window.title("Planar graph drawing on a grid")

        self.grid = None

        self.button = Button(self.window, text="Set window full screen and then click me", command=self.init_canvas)
        self.button.pack()

        self.window.mainloop()

    def init_canvas(self):
        self.window.update()
        self.grid = GridCanvas(self.window,
                               self.window.winfo_width(),
                               self.window.winfo_height() - self.button.winfo_height())
        self.grid.pack()
        self.button.configure(text="Change graph", command=self.change_graph)

    def update_display(self):
        self.grid.delete("all")
        self.grid.set_n(len(self.current_graph))
        if len(self.current_graph) < 25:
            self.grid.draw_grid()
        self.draw_graph()
        self.window.update()

    def draw_edge(self, u, v, color):
        self.grid.draw_edge(self.x_pos[u], self.y_pos[u], self.x_pos[v], self.y_pos[v], color)

    def add_text(self, v):
        self.grid.add_text(str(v+1), self.x_pos[v], self.y_pos[v])


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

    def draw_grid(self):
        for i in range(self.width):
            for j in range(self.height):
                self.draw_point(i, j)

    def draw_point(self, x, y):
        x_window, y_window = self.to_grid_coordinates(x, y)
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
