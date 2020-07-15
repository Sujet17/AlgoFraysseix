import networkx as nx
from typing import List, Tuple


def load_graph_list(file_path: str) -> List[nx.Graph]:
    graphs = []
    f = open(file_path, 'r')
    line = f.readline()
    current_graph = []
    while line != '':
        if line != "\n":
            current_graph.append(line[:-1])
        else:
            graphs.append(load_graph(current_graph))
            current_graph = []
        line = f.readline()
    graphs.append(load_graph(current_graph))
    f.close()
    return graphs


def load_graph(adj_lists: List[str]) -> nx.Graph:
    g = nx.Graph()
    g.add_nodes_from(range(len(adj_lists)))
    for adj_l in adj_lists:
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
    """Return a list of the planar embeddings of the graphs of the given list
    Non-planar graphs are ignored
    :param graph_list:
    :return:
    """
    result = []
    for graph in graph_list:
        planar, embedding = nx.check_planarity(graph)
        if planar:
            result.append(embedding)
    return result


def dict_pos_to_coord_list(positions: dict) -> Tuple[List[int], List[int]]:
    x_positions = [None] * len(positions)
    y_positions = [None] * len(positions)
    for v in positions:
        x, y = positions[v]
        x_positions[v] = x
        y_positions[v] = y
    return x_positions, y_positions
