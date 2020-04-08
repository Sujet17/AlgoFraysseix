#!/usr/bin/env python

from EmbeddedGraph import EmbeddedGraph


def get_canonical_ordering(g: EmbeddedGraph, external_face: tuple):
    """

    :param g: A graph coming with a planar embedding
    :param external_face: A tuple (v1, v2, v3) where v1, v2 and v3 are the vertices
        appearing on the outer boundary of the graph in the counterclockwise order
    :return: An ordering on the vertices that is canonical
    """
    v1, v2, vn = external_face

    chords = [0] * g.size  # For each vertex, the number of incident chords
    out = [False] * g.size  # out[v] is True iff v is on the outer boundary of the subgraph of g induced by the
    # vertices that are not in the order yet
    mark = [False] * g.size  # mark[v] is True iff v is already in the order

    available_vertices = []  # Not implemented yet, a list to store the possible candidates

    out[v1] = True
    out[v2] = True
    out[vn] = True

    result = []

    for k in range(g.size, 2, -1):

        x = get_available_vertex(g, mark, out, chords, v1, v2)
        mark[x] = True

        wpq = find_wpq(g, x, out, mark)
        # wpq = update_wi(g, wi, x)
        # wi = [w for w in g.getNeighbors(x) if not mark[w]]
        # print("x : ", x, " ; wpq: ", wpq)

        assert len(wpq) >= 2  # Not necessary, used while implementation

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

        result.insert(0, x)
    result.insert(0, v2)
    result.insert(0, v1)
    return result


def get_available_vertex(g, mark, out, chords, v1, v2):
    # print("out : ", out)
    # print("mark : ", mark)
    # print("chords: ", chords)
    for i in range(g.size):
        if is_available_vertex(i, mark, out, chords, v1, v2):
            return i
    raise Exception('not available vertex')


def is_available_vertex(x, mark, out, chords, v1, v2):
    return not mark[x] and out[x] and chords[x] == 0 and x != v1 and x != v2


def find_wpq(g: EmbeddedGraph, x: int, out: list, mark: list):
    """
    Find the list of the neighbors of x that are not marked yet. They appear consecutively on the external cycle.
    Among the neighbors of x, only two vertices are marked 'out' : they are wp and wq. So this method finds wp and wq
    and returns a list of the not marked neighbors with either wp or wq at the first position and the other at the last
    position.
    :param g: The graph
    :param x: The vertex that is added in the order
    :param out: The list that stores which vertex are 'out'
    :param mark: The list that stores which vertices are marked
    :return: A list
    """
    neighbors = g.neighbors(x)
    wp = None
    wq = None
    wpq = []
    for n in neighbors:
        if not mark[n]:
            wpq.append(n)
            if out[n]:
                if wp is None:
                    wp = len(wpq) - 1  # wp is the index of wp in wpq
                elif wq is None:
                    wq = len(wpq) - 1
                else:
                    raise InterruptedError("More than")  # Cannot append

    if len(wpq) > 2 and wq == wp + 1:
        wpq = wpq[wq:] + wpq[:wp + 1]
    return wpq
