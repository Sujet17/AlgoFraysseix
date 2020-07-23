import networkx as nx
from typing import List


def load_graph_list(file_path: str) -> List[nx.Graph]:
    """Read a file where a graph is given in adjacency list format and each graph is separated from its follower
    by an empty line.

    :param file_path:
    :return: The list of the graphs described in the file.
    """
    graphs = []
    f = open(file_path, 'r')
    line = f.readline()
    current_graph_lst = []
    while line != '':
        if line != "\n":
            current_graph_lst.append(line[:-1])
        else:
            graphs.append(load_graph(current_graph_lst))
            current_graph_lst = []
        line = f.readline()
    graphs.append(load_graph(current_graph_lst))
    f.close()
    return graphs


def load_graph_from_edges(file_path: str) -> nx.Graph:
    """Read a file whose each line is an edge of the graph.

    :param file_path:
    :return:
    """
    graph = nx.Graph()
    with open(file_path) as f:
        line = f.readline()
        while line != '':
            u, v = line.split(' ')
            graph.add_edge(int(u), int(v))
            line = f.readline()
    return graph


def load_graph(adj_list: List[str]) -> nx.Graph:
    """Read a list of strings which is an adjacency list and return the corresponding graph.

    :param adj_list: A list of strings of the form "x: a b c" where each string gives the neighbors (a,b,c in the
        example) of a vertex (x in the example).
    :return: The corresponding graph.
    """
    g = nx.Graph()
    g.add_nodes_from(range(len(adj_list)))
    for adj_l in adj_list:
        adj = adj_l.split(': ')
        if len(adj) == 2:
            v = int(adj[0]) - 1
            neighbors = adj[1].split(' ')
            for n in neighbors:
                u = int(n) - 1
                if v < u:
                    g.add_edge(v, u)
    return g


def embed_graph_list(graph_list: List[nx.Graph]) -> List[nx.PlanarEmbedding]:
    """Return a list of the planar embeddings of the graphs of the given list.
    Non-planar graphs and graphs whose size is smaller than 3 are ignored.
    :param graph_list:
    :return:
    """
    result = []
    for graph in graph_list:
        planar, embedding = nx.check_planarity(graph)
        if len(graph) > 2 and planar:
            result.append(embedding)
    return result
