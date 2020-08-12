import networkx as nx
from typing import Tuple, List
from networkx.algorithms.planar_drawing import triangulate_embedding
from canonical_ordering import get_canonical_ordering


def compute_pos(embedding: nx.PlanarEmbedding) -> Tuple[List[int], List[int]]:
    """Triangulates the graph, computes a canonical ordering and use it to compute a planar drawing on a grid.

    :param embedding: The planar embedding of the graph.
    :return:
        A tuple (x_pos, y_pos) where x_pos is a list that maps vertices to their x-positions and y_pos a list that maps
        vertices to their y-positions.
    """
    embedding_t, external_face = triangulate_embedding(embedding)
    ordering, wpq_list = get_canonical_ordering(embedding_t, external_face)
    x, y = shift_algorithm(ordering, wpq_list)
    return x, y


def shift_algorithm(ordering: List[int], wp_wq: List[List[int]]) -> Tuple[List[int], List[int]]:
    """Map every node to a (x, y) position.

    :param ordering: A canonical ordering of the vertices.
    :param wp_wq: A list that associates each vertex vk to the list of its neighbors appearing in the clockwise order
        on the external cycle of G_{k-1}.
    :return:
        A tuple (x_pos, y_pos) where x_pos is a list that maps vertices to their x-positions and y_pos a list that maps
        vertices to their y-positions.
    """
    # Initialization
    v1, v2, v3 = ordering[:3]
    left = ['N'] * len(ordering)
    right = ['N'] * len(ordering)
    offset = [None] * len(ordering)
    y = [None] * len(ordering)

    offset[v1] = 0
    y[v1] = 0
    right[v1] = v3
    left[v1] = None
    offset[v3] = 1
    y[v3] = 1
    right[v3] = v2
    left[v3] = None
    offset[v2] = 1
    y[v2] = 0
    right[v2] = None
    left[v2] = None

    # Phase 1: Install v3 to vn one by one.
    for k in range(3, len(ordering)):
        vk = ordering[k]
        neighbors_vk = wp_wq[k]
        wp = neighbors_vk[0]
        wq = neighbors_vk[-1]
        offset[neighbors_vk[1]] += 1
        offset[wq] += 1
        local_offset = sum([offset[i] for i in neighbors_vk[1:]])
        offset[vk] = 0.5 * (local_offset - y[wp] + y[wq])
        y[vk] = 0.5 * (local_offset + y[wp] + y[wq])
        offset[wq] = local_offset - offset[vk]

        if len(neighbors_vk) > 2:
            offset[neighbors_vk[1]] -= offset[vk]
        right[wp] = vk
        right[vk] = wq

        if len(neighbors_vk) > 2:
            left[vk] = neighbors_vk[1]
            right[neighbors_vk[-2]] = None
        else:
            left[vk] = None

    # Phase 2: Traverse the tree to compute the absolute x-positions.
    accumulate_offset(v1, 0, left, right, offset)
    return offset, y


def accumulate_offset(v: int, delta: int, left: list, right: list, offset: list):
    """Recursively compute the absolute x-coordinates of the vertices of the tree whose v is the root.

    :param v: The root of the given tree.
    :param left: The list that associates each vertex to its left child.
    :param right: The list that associates each vertex to its left child.
    :param offset: The list of x_positions
    :param delta: The absolute x-coordinate of the father of v in T
    """
    if v is not None:
        offset[v] += delta
        accumulate_offset(left[v], offset[v], left, right, offset)
        accumulate_offset(right[v], offset[v], left, right, offset)
