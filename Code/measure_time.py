import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from timeit import default_timer as timer
from typing import List, Tuple, Callable

from canonical_ordering import get_canonical_ordering
from load_graph import load_embedding_lst, get_graphs_without_edge
from shift_algorithm import compute_pos, triangulate_embedding, shift_algorithm
from main import MyParser


def measure_time(f: Callable) -> tuple:
    """Return the CPU time and the result of the execution of the given function.

    :param f: The executed function.
    :return: The execution time of the function.
    """
    start = timer()
    res = f()
    end = timer()
    return end - start, res


def time_to_compute(start_arg: tuple, repeat: int, *functions: Callable) -> tuple:
    """Measures the execution times of a list of functions.

    Each function takes as argument what the previous function in the list returns, except the first function that takes
    the elements of the tuples start_arg as arguments.

    :param start_arg: The tuple of the arguments of the first function.
    :param repeat: The whole list of functions will be executed as many times as repeat specified.
    :param functions: The list of function that will be tested.
    :return: A tuple that associates to each function its average execution time.
    """
    times = [0]*len(functions)
    for _ in range(repeat):
        r = start_arg
        for i, f in enumerate(functions):
            t, r = measure_time(lambda: f(*r))
            times[i] += t
    return tuple([t / repeat for t in times])


def time_to_compute_lst(embedding_lst: List[nx.PlanarEmbedding], repeat: int, triangulate: bool) \
        -> Tuple[List[int], List[float]]:
    """Plot the execution times of the shift algorithm for the graphs of the list.

    For each graph, this function measures the time necessary to compute its drawing.

    :param embedding_lst: The list of graphs to test.
    :param repeat: The number of times that the execution time is measured for each graph.
    :param triangulate: If this argument is true, the triangulation time will be counted in the measures. Else
    :return: The list of the sizes of the graphs tested and the list of the measures.
    """
    sizes = []
    times = []
    for embedding in embedding_lst:
        sizes.append(len(embedding))
        if triangulate:
            times.append(time_to_compute((embedding,), repeat, compute_pos))
        else:
            embedding_t, ext_face = triangulate_embedding(embedding)
            times.append(time_to_compute((embedding_t, ext_face), repeat, compute_pos))
    return sizes, times


# Specific function used only to measure the execution times of some graphs.
def __test():
    lst = load_embedding_lst(['graph_examples/generatedAll.lst', 'graph_examples/hog.lst'])
    lst += get_graphs_without_edge(1500)
    sizes, times1, times2 = [], [], []
    for g in lst:
        embedding, external_face = triangulate_embedding(g)
        t1, t2 = time_to_compute((embedding, external_face), 10, get_canonical_ordering, shift_algorithm)
        sizes.append(len(g))
        times1.append(t1)
        times2.append(t2)
    f = open('results1500genhog.txt', 'w')
    for i in range(len(sizes)):
        f.write(str(sizes[i]) + '-' + str(times1[i]) + '-' + str(times2[i]) + '\n')
    f.close()
    plot_results([(sizes, times1, 'Canonical order'),
                  (sizes, times2, 'Shift algorithm')])


def plot_results(result_lst: List[Tuple[List[int], List[float], str]], regression: bool = False):
    """Plot all the results given with matplotlib.

    :param result_lst: A list of tuples. Each tuples contains a list of results and a string that will be used to
        identify this list in the legend.
    :param regression: If this argument is True, a regression line of all the results will be drawn.
    :return:
    """
    plt.title("CPU time in function of the size of the graph")
    plt.xlabel("Graph size")
    plt.ylabel("CPU time (s)")

    all_times = []
    all_sizes = []

    for sizes, times, label in result_lst:
        plt.scatter(sizes, times, s=1, label=label)
        if regression:
            all_times += times
            all_sizes += sizes

    if regression:
        # Regression line: m = slope, p = intercept.
        m, p = np.polyfit(all_sizes, all_times, 1)
        x = np.array(all_sizes)
        plt.plot(x, m * x + p, linewidth=.5, label='Regression line : y = {:.2e} x  + {:.2e}'.format(m[0], p[0]))
    plt.legend()
    plt.show()


if __name__ == "__main__":
    parser = MyParser('Execute the shift-algorithm on the specified graphs and plot the execution times.')
    parser.add_argument('--repeat', type=int, default='1', help='The number of times each graph is tested. '
                                                                '(Default: 1)')

    parser.add_argument("-r", "--regression", action="store_true", help='Plot a regression line.')
    parser.add_argument("-t", "--triangulation", action="store_true", help='If specified, the triangulation time will '
                                                                           'be counted in the measures.')
    args = parser.parse_args()
    results = []
    nb_graphs = 0
    for name in args.files:
        graph_lst = load_embedding_lst([name], args.min, args.max)
        nb_graphs += len(graph_lst)
        results.append((*time_to_compute_lst(graph_lst, args.repeat, args.triangulation), name))
    if nb_graphs > 0:
        plot_results(results, args.regression)
    else:
        print("There is no graph to treat")
