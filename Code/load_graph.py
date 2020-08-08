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


def save_graph_lst(graph_lst: List[nx.Graph], file_path: str):
    """Write a list of graphs on a file.

    Each graph is writen as a list of consecutive lines where each line gives the neighbors of a vertex v under the form
    'v: a b c'. An empty line separates each graph from the others. The vertices of the graphs must be integers from 0
    to n-1. If the file is not empty, the graph list will be append after the existing content of the file.

    :param graph_lst: The list of graphs that will be saved.
    :param file_path: The path of the file.
    :return:
    """
    f = open(file_path, 'a')
    for graph in graph_lst:
        s = get_graph_as_str(graph)
        f.write(s)
    f.close()


def get_graph_as_str(graph: nx.Graph) -> str:
    """Transpose the graph into a string.

    Each line of the string gives the neighbors of a vertex v under the form 'v: a b c'. The vertices of the graph must
    be integers from 0 to n-1. The vertices in the string will be integers from 1 to n.

    :param graph: A graph whose vertices must be integers from 0 to n-1.
    :return: The graph writen as an string.
    """
    graph_as_str = ""
    for i in range(len(graph)):
        graph_as_str += str(i+1) + ':'
        for n in graph.neighbors(i):
            graph_as_str += ' ' + str(n+1)
        graph_as_str += '\n'
    return graph_as_str


def convert_format(input_file_path: str, output_file_path: str):
    """Read a graph in input_file and write it in an other format on output_file.

    The input file format is one edge 'a b' per line, and the first line is ignored. In the output file each line gives
    the neighbors of a vertex v under the form 'v: a b c', with a blank line at the end. If the output file is not
    empty, the graph will be append after the existing content of the file.

    :param input_file_path: The path of the input file.
    :param output_file_path: The path of the output file.
    :return:
    """
    graph = load_graph_from_edges(input_file_path)
    save_graph_lst([graph], output_file_path)


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
            graph.add_edge(int(u)-1, int(v)-1)
            line = f.readline()
    return graph


def embed_graph_list(graph_list: List[nx.Graph]) -> List[nx.PlanarEmbedding]:
    """Return a list of the planar embeddings of the graphs of the given list.

    Non-planar graphs and graphs whose size is smaller than 3 are ignored.

    :param graph_list: A list of graphs.
    :return: The list of the planar embeddings.
    """
    result = []
    for graph in graph_list:
        planar, embedding = nx.check_planarity(graph)
        if len(graph) > 2 and planar:
            result.append(embedding)
    return result


def get_embeddings_from_files(file_names: List[str], min_size=None, max_size=None) -> List[nx.PlanarEmbedding]:
    graph_list = []
    for file in file_names:
        g_lst = embed_graph_list(load_graph_list(file))
        for g in g_lst:
            if (min_size is None or len(g) > max(2, min_size)) and (max_size is None or len(g) < max_size):
                graph_list.append(g)
    return graph_list
