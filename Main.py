#!/usr/bin/env python

from tkinter import *
from nonOrientedGraph import *
from canonicalOrdering import *
from graphsExamples import *
from shilftAlgorithm import ShiftAlgorithm
from planarityTest import DFS
N = 20
CELL_SIZE = 30


class App:
    def __init__(self):
        self.window = Tk()
        self.window.title("Algo de de Fraisseyx")
        self.grid = GridCanvas(self.window, N, CELL_SIZE)
        self.grid.pack()

        button = Button(self.window, text="Change graph", command=self.change_graph)
        button.pack()
        self.bool = TRUE
        self.change_graph()

    def change_graph(self):
        if self.bool:
            g = load_graph4()
            external_face = (0, 1, 15)
            self.bool = False
        else:
            g = load_graph3()
            external_face = (0, 1, 2)
            self.bool = True

        ordering = get_canonical_ordering(g, external_face)
        algo = ShiftAlgorithm(g, ordering)
        xpos, ypos = algo.run()
        self.grid.draw_graph(g, xpos, ypos)
        self.window.update()

    def run(self):
        self.window.mainloop()


class GridCanvas(Canvas):
    def __init__(self, parent, n, cell_size):
        self.width = 2 * n - 4
        self.height = n - 2
        Canvas.__init__(self, parent, width=(self.width + 1) * cell_size, height=(self.height + 1) * cell_size)
        self.n = n
        self.cell_size = cell_size

        self.draw_grid()

    def display_borders(self):
        h = (self.height + 1) * self.cell_size
        w = (self.width + 1) * self.cell_size

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

    def draw_edge(self, x1, y1, x2, y2):
        x1_window, y1_window = self.to_grid_coordinates(x1, y1)
        x2_window, y2_window = self.to_grid_coordinates(x2, y2)
        self.create_line(x1_window, y1_window, x2_window, y2_window, fill='red')

    def to_grid_coordinates(self, x, y):
        return (x + 1) * self.cell_size, (self.height - (y + 1)) * self.cell_size

    def add_text(self, txt, x, y):
        x_window, y_window = self.to_grid_coordinates(x, y)
        self.create_text(x_window, y_window, text=txt)

    def draw_graph(self, g, x_coord, y_coord):
        self.delete("all")
        self.draw_grid()
        for i in range(g.size):
            self.add_text(str(i), x_coord[i], y_coord[i])
            for n in g.neighbors(i):
                if n > i:
                    self.draw_edge(x_coord[i], y_coord[i], x_coord[n], y_coord[n])


if __name__ == "__main__":
    app = App()
    """
    G = load_graph1()
    dfs = DFS(G)
    print(dfs.get_ordering())
    """

    """
    print("-------")

    for i in range(G.size):
        print(G.neighbors(i))

    print("-------")
    """
    app.run()
