import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from timeit import default_timer as timer
from typing import List
from load_graph import load_graph_list, embed_graph_list, get_embeddings_from_files
from shift_algorithm import compute_pos
from main import MyParser


def test_time(embedding_lst: List[nx.PlanarEmbedding], repeat: int):
    """Plot the execution times of the shift algorithm for the graphs of the list.

    For each graph, this function calculates its straight line drawing and plots the average execution time.

    :param embedding_lst:
    :param repeat: The number of times that the execution time is measured for each graph.
    :return:
    """
    sizes = []
    times = []
    for embedding in embedding_lst:
        time = 0
        for _ in range(repeat):
            start = timer()
            compute_pos(embedding)
            end = timer()
            time += end - start
        sizes.append(len(embedding))
        times.append(time/repeat)

    plt.xlabel("Graph size")
    plt.ylabel("CPU time(s)")
    plt.scatter(sizes, times, s=2)

    # Regression line: m = slope, b = intercept.
    m, b = np.polyfit(sizes, times, 1)
    x = np.array(sizes)
    plt.plot(x, m * x + b, color='orange', linewidth=.5)
    plt.show()


if __name__ == "__main__":
    parser = MyParser('Execute the shift-algorithm on the specified graphs and plot the execution times.')
    parser.add_argument('-r', '--repeat', type=int, default='1', help='The number of times each graph is tested. '
                                                                      '(Default: 1)')
    args = parser.parse_args()
    files = ['graph_examples/'+name for name in args.files]
    graph_list = get_embeddings_from_files(files, args.min, args.max)
    if len(graph_list) > 0:
        test_time(graph_list, args.repeat)
