import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from timeit import default_timer as timer
from typing import List
from shift_algorithm import compute_pos


def test_time(embedding_list: List[nx.PlanarEmbedding]):
    sizes = []
    times = []
    i = 0
    for embedding in embedding_list:
        start = timer()
        compute_pos(embedding)
        end = timer()
        time = end - start
        sizes.append(len(embedding))
        times.append(time)

    plt.xlabel("Taille du graphe")
    plt.ylabel("Temps CPU (s)")
    plt.scatter(sizes, times, s=2)

    # Regression line: m = slope, b = intercept.
    m, b = np.polyfit(sizes, times, 1)
    x = np.array(sizes)
    plt.plot(x, m * x + b, color='orange')
    plt.show()
