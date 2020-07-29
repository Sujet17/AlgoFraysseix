import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from timeit import default_timer as timer
from typing import List

from load_graph import load_graph_list, embed_graph_list
from shift_algorithm import compute_pos


def test_embedding_list(embedding_list):
    for i, embedding in enumerate(embedding_list):
        try:
            compute_pos(embedding)
        except ValueError:
            print("VALUE ERROR")
            for j in embedding.nodes:
                print(j, ':', sorted([n for n in embedding.neighbors(j)]))
            return False
        except IndexError:
            print("INDEX ERROR")
            for j in embedding.nodes:
                print(j, ':', sorted([n for n in embedding.neighbors(j)]))
            return False
    return True


def test():
    graphs = load_graph_list("hog_planar_graphs.lst")
    print(len(graphs))
    embeddings = embed_graph_list(graphs)
    print(len(embeddings))
    print("LOADED AND EMBEDDED")
    if test_embedding_list(embeddings):
        print("OK")


def test_time(file_paths: str):
    """Plot the execution times of the shift algorithm for the graphs of the list.

    :param file_paths:
    :return:
    """
    embedding_lst = []
    for file_path in file_paths:
        embedding_lst += embed_graph_list(load_graph_list(file_path))
    sizes = []
    times = []
    i = 0
    for embedding in embedding_lst:
        start = timer()
        compute_pos(embedding)
        end = timer()
        time = end - start
        sizes.append(len(embedding))
        times.append(time)

    plt.xlabel("Graph size")
    plt.ylabel("CPU time(s)")
    plt.scatter(sizes, times, s=2)

    # Regression line: m = slope, b = intercept.
    m, b = np.polyfit(sizes, times, 1)
    x = np.array(sizes)
    plt.plot(x, m * x + b, color='orange')
    plt.show()


def find_planar_subgraph(graph: nx.Graph) -> nx.PlanarEmbedding:
    if len(graph) < 3:
        return graph
    else:
        is_planar_boolean, bad_minor = nx.check_planarity(graph, True)
        if is_planar_boolean:
            return graph
        else:
            graph.remove_node(bad_minor[0])
            return find_planar_subgraph(graph)


#while True:
#    nx.gnp_random_graph(1000, 0.2)
#    nx.fast_gnp_random_graph()
