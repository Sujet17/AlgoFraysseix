import networkx as nx
from typing import List, Tuple


def get_canonical_ordering(g: nx.PlanarEmbedding, external_face: tuple) -> List[Tuple[int, list]]:
    """Returns a canonical ordering of the nodes

    :param g: A triangulated graph coming with a planar embedding
    :param external_face: A tuple (v1, v2, v3) where v1, v2 and v3 are the vertices
        appearing on the outer boundary of the graph in the counterclockwise order
    :return: An ordering on the vertices that is canonical
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

    available_vertices = []  # Not implemented yet, a list to store the possible candidates

    out[v1] = True
    out[v2] = True
    out[vn] = True

    ordering = [None] * len(g)
    ordering[0] = v1, []
    ordering[1] = v2, []

    for k in range(len(g), 2, -1):

        x = pick_available_vertex(g, mark, out, chords, v1, v2)
        mark[x] = True

        if k == len(g):
            wpq = find_wpq(g, x, out, mark, v2)
        else:
            wpq = find_wpq(g, x, out, mark)

        # print("x : ", x, " ; wpq: ", wpq)
        # assert len(wpq) >= 2  # Not necessary, used while implementation

        if len(wpq) == 2:
            for w in wpq:
                out[w] = True
                chords[w] -= 1
        else:
            for i in range(len(wpq)):
                w = wpq[i]
                out[w] = True

                if 0 < i < len(wpq) - 1:
                    neighbors = g.neighbors(w)
                    for n in neighbors:
                        if not mark[n] and out[n] and n != wpq[i - 1] and n != wpq[i + 1]:
                            chords[w] += 1
                            if n not in wpq[1:-1]:
                                chords[n] += 1

        ordering[k-1] = x, wpq

    return ordering


def pick_available_vertex(g, mark, out, chords, v1, v2):
    # print("out : ", out)
    # print("mark : ", mark)
    # print("chords: ", chords)
    for i in range(len(g)):
        if is_available_vertex(i, mark, out, chords, v1, v2):
            return i
    raise Exception('not available vertex')


def is_available_vertex(x, mark, out, chords, v1, v2):
    return not mark[x] and out[x] and chords[x] == 0 and x != v1 and x != v2


def find_wpq(g: nx.PlanarEmbedding, v: int, out: list, mark: list, wq=None):
    """
    Find the list of the neighbors of x that are not marked yet. They appear consecutively on the external cycle.

    Among the neighbors of x, only two vertices are marked 'out' : they are wp and wq. So this method finds wp and wq
    and returns a list of the not marked neighbors with either wp or wq at the first position and the other at the last
    position.

    :param g: The graph
    :param v: The vertex that is added in the order
    :param out: The list that stores which vertex are 'out'
    :param mark: The list that stores which vertices are marked
    :param wq: For the first vertex, we know that wq is v2. For the other vertices, wq is not specified
    :return: A list of the non-marked neighbors of x, in the counterclockwise order looking from x
    """
    wpq = []
    neighbors = list(g.neighbors_cw_order(v))
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

    wq_index = out_wpq_indices[1]
    if wq is not None:  # If wq is specified in the arguments
        if wq == neighbors[out_neighbors_indices[0]]:
            wq_index = out_wpq_indices[0]
    else:
        # Except for the first vertex, there is always a neighbor of v that is marked. So, as the first vertex case is
        # managed, we can identify wq as the out_vertex that is preceded by a marked vertex in the list of neighbors.
        if mark[neighbors[out_neighbors_indices[0]-1]]:
            wq_index = out_wpq_indices[0]

    wpq = wpq[wq_index:] + wpq[:wq_index]
    wpq.reverse()
    return wpq