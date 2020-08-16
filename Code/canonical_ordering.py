import networkx as nx
from typing import List, Tuple


def get_canonical_ordering(g: nx.PlanarEmbedding, external_face: tuple) -> Tuple[List[int], List[List[int]]]:
    """Returns a canonical ordering of the nodes of the graph.

    :param g: A triangulated graph coming with a planar embedding.
    :param external_face: A tuple (v1, v2, v3) where v1, v2 and v3 are the vertices
        appearing on the outer boundary of the graph in the counterclockwise order.
    :return: An ordering on the vertices that is canonical and a list that associates to each vertex vk its neighbors on
        the external cycle of G_{k-1}.
    """
    v1, v2, vn = external_face
    # For each vertex v:
    # - chords[v] is the number of incident chords to v.
    # - out[v] is True iff v is on the outer boundary of the subgraph of g induced by the
    #   vertices that are not in the order yet
    # - mark[v] is True iff v is already in the order
    chords = [0] * len(g)
    out = [False] * len(g)
    mark = [False] * len(g)

    available_vertices = set([vn])

    out[v1] = True
    out[v2] = True
    out[vn] = True

    chords[v1] = 1
    chords[v2] = 1

    ordering = [None] * len(g)
    ordering[0] = v1
    ordering[1] = v2
    # wp_wq associates each vertex v[k] to its neighbors on G_{k-1}, i.e., if ordering[k] = vk, wp_wq[k]
    # is the list of the neighbors of vk.
    wp_wq = [[] for i in range(len(g))]

    for k in range(len(g), 2, -1):

        vk = available_vertices.pop()
        mark[vk] = True

        if k == len(g):
            wpq = find_wpq(g, vk, out, mark, v1)
        else:
            wpq = find_wpq(g, vk, out, mark)

        if len(wpq) == 2:
            for w in wpq:
                chords[w] -= 1
                if chords[w] == 0:
                    available_vertices.add(w)
        else:
            new_face_nodes_lst = wpq[1:-1]
            new_face_nodes = set(new_face_nodes_lst)
            for w in new_face_nodes_lst:
                out[w] = True

            for i, w in enumerate(new_face_nodes_lst):
                available_vertex = True
                neighbors = g.neighbors(w)
                for n in neighbors:
                    if not mark[n] and out[n] and n != wpq[i] and n != wpq[i + 2]:
                        # (w, n) is a chord
                        chords[w] += 1
                        available_vertex = False
                        if n not in new_face_nodes:
                            chords[n] += 1
                            available_vertices.discard(n)
                if available_vertex:
                    available_vertices.add(w)
        ordering[k-1] = vk
        wp_wq[k-1] = wpq
    return ordering, wp_wq


def find_wpq(g: nx.PlanarEmbedding, v: int, out: list, mark: list, wp: int = None):
    """
    Find the list of the neighbors of x that are not marked yet. They appear consecutively on the external cycle.

    Among the neighbors of x, only two vertices are marked 'out' : they are wp and wq. So this method finds wp and wq
    and returns a list of the not marked neighbors with either wp at the first position and wq at the last position.

    :param g: The graph
    :param v: The vertex that is added in the order
    :param out: The list that stores which vertex are 'out'
    :param mark: The list that stores which vertices are marked
    :param wp: For the first vertex, we know that wp is v1. For the other vertices, wp is not specified
    :return: A list of the non-marked neighbors of x, in the counterclockwise order looking from x
    """
    wpq = []
    neighbors = list(neighbors_ccw_order(g, v))
    # x has exactly two neighbors that are 'out'. There are wp and wq, i.e., the first and last vertices of wpq
    # out_wpq_indices stores the indices of the two out vertices in wpq
    # out_neighbors_indices stores the indices of the two out vertices in the neighbors list
    out_wpq_indices = []
    out_neighbors_indices = []

    for i, n in enumerate(neighbors):
        if not mark[n]:
            wpq.append(n)
            if out[n]:
                out_wpq_indices.append(len(wpq) - 1)
                out_neighbors_indices.append(i)

    wp_index = out_wpq_indices[1]
    if wp is not None:
        # If wq is specified in the arguments.
        if wp == neighbors[out_neighbors_indices[0]]:
            wp_index = out_wpq_indices[0]
    else:
        # Except for the first vertex, there is always a neighbor of v that is marked. So, as the first vertex case is
        # managed, we can identify wq as the out_vertex that is preceded by a marked vertex in the list of neighbors.
        if mark[neighbors[out_neighbors_indices[0]-1]]:
            wp_index = out_wpq_indices[0]

    wpq = wpq[wp_index:] + wpq[:wp_index]
    return wpq


def neighbors_ccw_order(embedding: nx.PlanarEmbedding, v: int):
    """Generator for the neighbors of v in counter-clockwise order.

    :param embedding:
    :param v:
    :return:
    """
    if len(embedding[v]) == 0:
        return
    start_node = embedding.nodes[v]['first_nbr']
    yield start_node
    current_node = embedding[v][start_node]['ccw']
    while start_node != current_node:
        yield current_node
        current_node = embedding[v][current_node]['ccw']
