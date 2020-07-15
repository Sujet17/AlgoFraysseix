import networkx as nx
from networkx.algorithms.planar_drawing import triangulate_embedding


def triangulate(embedding: nx.PlanarEmbedding):
    """Triangulates the embedding.

    :param embedding: A connected graph with a planar embedding
    :return:
    """
    for v in embedding.nodes:
        neighbors = embedding.neighbors(v)
        for i, n in enumerate(neighbors):
            n2 = neighbors[(i+1) % len(neighbors)]
            if True:
                embedding.add_dummy_edge()
    sorted_edges = bucket_sort(embedding)
    remove_multiple_edges(embedding, sorted_edges)


def bucket_sort(g: nx.PlanarEmbedding) -> list:
    """

    :param g:
    :return:
    """
    edge_list = []
    for v in g.vertices():
        for n in g.adj(v):
            edge_list.append((v, n))
    for i in [1, 0]:
        bucket = [[] for j in range(g.size)]
        while len(edge_list) > 0:
            edge = edge_list.pop()
            bucket[edge[i]].append(edge)
        for j in range(g.size):
            edge_list += bucket[j]
    return edge_list


def remove_multiple_edges(g: nx.PlanarEmbedding, sorted_edges: list):
    for i, edge in enumerate(sorted_edges):
        if edge == edge[i+1]:
            pass
