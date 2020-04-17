from nonOrientedGraph import Graph
from EmbeddedGraph import EmbeddedGraph


def load_graph1():
    graph = Graph(6)

    graph.add_edge(0, 1)
    graph.add_edge(0, 2)
    graph.add_edge(0, 3)

    graph.add_edge(1, 2)
    graph.add_edge(1, 3)

    graph.add_edge(2, 3)
    graph.add_edge(2, 4)
    graph.add_edge(2, 5)

    graph.add_edge(3, 5)

    graph.add_edge(4, 5)

    return graph


def load_graph2():
    graph = Graph(16)

    graph.add_edge(0, 1)
    graph.add_edge(0, 2)
    graph.add_edge(0, 6)
    graph.add_edge(0, 7)
    graph.add_edge(0, 8)
    graph.add_edge(0, 14)
    graph.add_edge(0, 15)

    graph.add_edge(1, 2)
    graph.add_edge(1, 3)
    graph.add_edge(1, 4)
    graph.add_edge(1, 5)
    graph.add_edge(1, 15)

    graph.add_edge(2, 3)
    graph.add_edge(2, 6)
    graph.add_edge(2, 9)

    graph.add_edge(3, 4)
    graph.add_edge(3, 9)
    graph.add_edge(3, 10)
    graph.add_edge(3, 11)
    graph.add_edge(3, 12)

    graph.add_edge(4, 5)
    graph.add_edge(4, 10)

    graph.add_edge(5, 10)
    graph.add_edge(5, 13)
    graph.add_edge(5, 15)

    graph.add_edge(6, 7)
    graph.add_edge(6, 9)

    graph.add_edge(7, 8)
    graph.add_edge(7, 9)

    graph.add_edge(8, 9)
    graph.add_edge(8, 14)

    graph.add_edge(9, 12)
    graph.add_edge(9, 14)

    graph.add_edge(10, 11)
    graph.add_edge(10, 13)

    graph.add_edge(11, 12)
    graph.add_edge(11, 13)

    graph.add_edge(12, 13)
    graph.add_edge(12, 14)
    graph.add_edge(12, 15)

    graph.add_edge(13, 15)

    graph.add_edge(14, 15)

    return graph


def load_graph3():
    graph = EmbeddedGraph(6)

    graph.add_edge(0, 2)
    graph.add_edge(0, 3)
    graph.add_edge(0, 5)
    # graph.add_edge(0, 4)
    graph.add_edge(0, 1)

    graph.add_edge(1, 0)
    graph.add_edge(1, 4)
    graph.add_edge(1, 2)

    graph.add_edge(2, 1)
    graph.add_edge(2, 4)
    graph.add_edge(2, 3)
    graph.add_edge(2, 0)

    graph.add_edge(3, 2)
    graph.add_edge(3, 4)
    graph.add_edge(3, 5)
    graph.add_edge(3, 0)

    graph.add_edge(4, 1)
    # graph.add_edge(4, 0)
    graph.add_edge(4, 5)
    graph.add_edge(4, 3)
    graph.add_edge(4, 2)

    graph.add_edge(5, 4)
    graph.add_edge(5, 0)
    graph.add_edge(5, 3)

    return graph


def load_graph4():
    graph = EmbeddedGraph(16)

    graph.add_edge(0, 15)
    graph.add_edge(0, 14)
    graph.add_edge(0, 8)
    graph.add_edge(0, 7)
    graph.add_edge(0, 6)
    graph.add_edge(0, 2)
    graph.add_edge(0, 1)

    graph.add_edge(1, 0)
    graph.add_edge(1, 2)
    graph.add_edge(1, 3)
    graph.add_edge(1, 4)
    graph.add_edge(1, 5)
    graph.add_edge(1, 15)

    graph.add_edge(2, 6)
    graph.add_edge(2, 9)
    graph.add_edge(2, 3)
    graph.add_edge(2, 1)
    graph.add_edge(2, 0)

    graph.add_edge(3, 12)
    # graph.add_edge(3, 11)
    graph.add_edge(3, 10)
    graph.add_edge(3, 4)
    graph.add_edge(3, 1)
    graph.add_edge(3, 2)
    graph.add_edge(3, 9)

    graph.add_edge(4, 1)
    graph.add_edge(4, 3)
    graph.add_edge(4, 10)
    graph.add_edge(4, 5)

    graph.add_edge(5, 1)
    graph.add_edge(5, 4)
    graph.add_edge(5, 10)
    graph.add_edge(5, 13)
    graph.add_edge(5, 15)

    graph.add_edge(6, 0)
    graph.add_edge(6, 7)
    graph.add_edge(6, 9)
    graph.add_edge(6, 2)

    graph.add_edge(7, 0)
    graph.add_edge(7, 8)
    graph.add_edge(7, 9)
    graph.add_edge(7, 6)

    graph.add_edge(8, 14)
    # graph.add_edge(8, 9)
    graph.add_edge(8, 7)
    graph.add_edge(8, 0)

    graph.add_edge(9, 3)
    graph.add_edge(9, 2)
    graph.add_edge(9, 6)
    graph.add_edge(9, 7)
    # graph.add_edge(9, 8)
    graph.add_edge(9, 14)
    graph.add_edge(9, 12)

    graph.add_edge(10, 5)
    graph.add_edge(10, 4)
    graph.add_edge(10, 3)
    graph.add_edge(10, 11)
    graph.add_edge(10, 13)

    graph.add_edge(11, 10)
    # graph.add_edge(11, 3)
    graph.add_edge(11, 12)
    graph.add_edge(11, 13)

    graph.add_edge(12, 11)
    graph.add_edge(12, 3)
    graph.add_edge(12, 9)
    graph.add_edge(12, 14)
    graph.add_edge(12, 15)
    graph.add_edge(12, 13)

    graph.add_edge(13, 12)
    graph.add_edge(13, 15)
    graph.add_edge(13, 5)
    graph.add_edge(13, 10)
    graph.add_edge(13, 11)

    graph.add_edge(14, 9)
    graph.add_edge(14, 8)
    graph.add_edge(14, 0)
    graph.add_edge(14, 15)
    graph.add_edge(14, 12)

    graph.add_edge(15, 1)
    graph.add_edge(15, 5)
    graph.add_edge(15, 13)
    graph.add_edge(15, 12)
    graph.add_edge(15, 14)
    graph.add_edge(15, 0)

    return graph


def load_graph5() -> EmbeddedGraph:
    graph = EmbeddedGraph(4)

    graph.add_edge(0, 3)
    graph.add_edge(0, 1)
    graph.add_edge(1, 0)
    graph.add_edge(1, 2)
    graph.add_edge(2, 1)
    graph.add_edge(2, 3)
    graph.add_edge(3, 2)
    graph.add_edge(3, 0)

    return graph
