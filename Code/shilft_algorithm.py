from typing import Tuple, List


def shift_algorithm(ordering: List[Tuple[int, list]]) -> Tuple[list, list]:
    v1, v2, v3 = [c[0] for c in ordering[:3]]
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

    phase1(ordering, left, right, offset, y)
    accumulate_offset(v1, 0, left, right, offset)
    return offset, y


def phase1(ordering: List[Tuple[int, list]], left: list, right: list, offset: list, y: list):
    """

    :param ordering:
    :param left:
    :param right:
    :param offset:
    :param y:
    :return:
    """
    for k in range(3, len(ordering)):
        vk, neighbors_wi = ordering[k]
        wp = neighbors_wi[0]
        wq = neighbors_wi[-1]
        offset[neighbors_wi[1]] += 1
        offset[wq] += 1
        local_offset = sum([offset[i] for i in neighbors_wi[1:]])
        offset[vk] = 0.5 * (local_offset - y[wp] + y[wq])
        y[vk] = 0.5 * (local_offset + y[wp] + y[wq])
        offset[wq] = local_offset - offset[vk]

        if len(neighbors_wi) > 2:
            offset[neighbors_wi[1]] -= offset[vk]
        right[wp] = vk
        right[vk] = wq

        if len(neighbors_wi) > 2:
            left[vk] = neighbors_wi[1]
            right[neighbors_wi[-2]] = None
        else:
            left[vk] = None


def accumulate_offset(v: int, delta: int, left: list, right: list, offset: list):
    """Compute the absolute x-coordinates of the vertices through a traversal of the tree.

    :param v:
    :param left:
    :param right:
    :param offset:
    :param delta:
    :return:
    """
    if v is not None:
        offset[v] += delta
        accumulate_offset(left[v], offset[v], left, right, offset)
        accumulate_offset(right[v], offset[v], left, right, offset)
