import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from timeit import default_timer as timer
from typing import List, Tuple

from canonical_ordering import get_canonical_ordering
from load_graph import get_embeddings_from_files
from shift_algorithm import compute_pos, triangulate_embedding, shift_algorithm
from main import MyParser


def time_to_compute_graph(g: nx.PlanarEmbedding, repeat: int) -> Tuple[int, float]:
    """

    :param g:
    :param repeat:
    :return: A tuple (size, avg_time)
    """
    time = 0
    for _ in range(repeat):
        start = timer()
        compute_pos(g)
        end = timer()
        time += end - start
    return len(g), time / repeat


def time_to_compute_graph_step(g: nx.PlanarEmbedding, repeat: int):
    t1, t2, t3 = 0, 0, 0
    for _ in range(repeat):
        start = timer()
        embedding_t, external_face = triangulate_embedding(g)
        end = timer()
        t1 += end - start
        start = timer()
        ordering, wpq_list = get_canonical_ordering(embedding_t, external_face)
        end = timer()
        t2 += end - start
        start = timer()
        x, y = shift_algorithm(ordering, wpq_list)
        end = timer()
        t3 += end - start
    return len(g), t1 / repeat, t2 / repeat, t3 / repeat


def time_to_compute_lst(embedding_lst: List[nx.PlanarEmbedding], repeat: int) -> Tuple[List[int], List[float]]:
    """Plot the execution times of the shift algorithm for the graphs of the list.

    For each graph, this function calculates its straight line drawing and plots the average execution time.

    :param embedding_lst:
    :param repeat: The number of times that the execution time is measured for each graph.
    :return:
    """
    sizes = []
    times = []
    for embedding in embedding_lst:
        size, time = time_to_compute_graph(embedding, repeat)
        sizes.append(size)
        times.append(time)
    return sizes, times


def plot_results(results: List[Tuple[List[int], List[float], str]], regression: bool = False):
    plt.title("CPU time in function of the size of the graph")
    plt.xlabel("Graph size")
    plt.ylabel("CPU time (s)")

    all_times = []
    all_sizes = []

    for sizes, times, label in results:
        plt.scatter(sizes, times, s=1, label=label)
        if regression:
            all_times += times
            all_sizes += sizes

    if regression:
        # Regression line: m = slope, p = intercept.
        m, p = np.polyfit(all_sizes, all_times, 1)
        x = np.array(all_sizes)
        plt.plot(x, m * x + p, linewidth=.5, label='Regression line : y = {:.2e} x  + {:.2e}'.format(m, p))
    plt.legend()
    plt.show()


def test_graphs_without_edge(largest: int = 750):
    sizes = []
    times = []
    for i in range(3, largest):
        g = nx.Graph()
        g.add_nodes_from(range(i))
        _, embedding = nx.check_planarity(g)
        size, time = time_to_compute_graph(embedding, 3)
        sizes.append(size)
        times.append(time)
        print(size)
    f = open('test1500.txt0', 'w')
    for i in range(len(times)):
        f.write(str(sizes[i]) + '-' + str(times[i]) + '\n')
    f.close()
    plot_results(sizes, times)
    return sizes, times


def plot_all():
    f = open('test1500.txt0', 'r')
    lines = f.readlines()
    f.close()
    sizes1 = []
    times1 = []
    for line in lines:
        size, time = line.split('-')
        sizes1.append(int(size))
        times1.append(float(time))

    r1 = sizes1, times1, 'Graphs without edge'
    r2 = (*time_to_compute_lst(get_embeddings_from_files(['graph_examples/hog_planar_graphs.lst']), 3)
          , 'Graphs from House of graphs')
    r3 = (*time_to_compute_lst(get_embeddings_from_files(['graph_examples/generated.lst'], max_size=8000), 3)
          , 'Random generated graphs')

    plot_results([r1, r2, r3], True)


if __name__ == "__main__":
    parser = MyParser('Execute the shift-algorithm on the specified graphs and plot the execution times.')
    parser.add_argument('--repeat', type=int, default='1', help='The number of times each graph is tested. '
                                                                '(Default: 1)')

    parser.add_argument("-r", "--regression", action="store_true", help='Plot a regression line.')
    args = parser.parse_args()
    results = []
    nb_graphs = 0
    for name in args.files:
        graph_lst = get_embeddings_from_files(['graph_examples/' + name], args.min, args.max)
        nb_graphs += len(graph_lst)
        results.append((*time_to_compute_lst(graph_lst, args.repeat), name))
    if nb_graphs > 0:
        plot_results(results, args.regression)
    else:
        print("There is no graph to treat")
