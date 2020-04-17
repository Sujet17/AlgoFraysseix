#!/usr/bin/env python

from EmbeddedGraph import EmbeddedGraph


def add_to_list(x, l):
    if x not in l:
        l.append(x)


class CanonicalTriangulation:
    def __init__(self, g: EmbeddedGraph):
        self.g = g
        self.ext_circle = []
        self.canonical_order = []
        self.marked = [False] * self.g.size

    def canonical_triangulate(self):
        old = [0] * self.g.size
        visit = [0] * self.g.size
        readylist = []
        v1, v2 = 0, 1
        self.ext_circle = [v1, v2]
        self.canonical_order = [v1, v2]

        # neighbors_marked = [0] * self.g.size
        self.marked[v1] = True
        self.marked[v2] = True
        for n in self.g.neighbors(v1):
            old[n] += 1
            # neighbors_marked[n] += 1
        for n in self.g.neighbors(v2):
            old[n] += 1
            # neighbors_marked[n] += 1
        readylist.append(self.rightup(0))
        add_to_list(self.leftup(1), readylist)

        for k in range(2, self.g.size):
            vk = readylist.pop()
            print('readylist : ', readylist, ' ; vk : ', vk)
            print('circle : ', self.ext_circle)
            self.canonical_order.append(vk)
            for n in self.g.neighbors(vk):
                # neighbors_marked[n] += 1
                if not self.marked[n]:
                    try:
                        readylist.remove(n)
                    except ValueError:
                        pass
                    old[n] += 1

            i, j = self.left_and_right_vertices(vk)
            left_connected = 1  # left_connected is 1 if there is an edge between leftvertex and vk, 0 else
            right_connected = 1

            # print("leftup - rightup : ", self.leftup(i), self.rightup(i), i, j)

            if i == j:
                if vk == self.leftup(i) and self.ext_circle[i] != v1:
                    # j = i
                    i -= 1
                    left_connected = 0
                elif vk == self.rightup(j) and self.ext_circle[j] != v2:
                    # i = j
                    j += 1
                    right_connected = 0
                else:
                    raise Exception("Unexpected situation")

            if vk == 11:
                print("ROLORLO ", self.ext_circle[i], old[10])
            # while neighbors_marked[self.ext_circle[i]] == self.g.degree(self.ext_circle[i]) \
            while old[self.ext_circle[i]] + left_connected == self.g.degree(self.ext_circle[i]) \
                    and self.ext_circle[i] != v1:
                i -= 1
                left_connected = 0
            # while neighbors_marked[self.ext_circle[j]] == self.g.degree(self.ext_circle[j]) \
            while old[self.ext_circle[j]] + right_connected == self.g.degree(self.ext_circle[j]) \
                    and self.ext_circle[j] != v2:
                j += 1
                right_connected = 0

            for ind in range(i, j + 1):
                ci = self.ext_circle[ind]
                if ci not in self.g.neighbors(vk):
                    if ind == i:
                        print('URG')
                        ci_successor = None
                        for it in range(self.g.degree(vk) - 1, -1, -1):
                            n = self.g.neighbors(vk)[it]
                            # print('it',it,'n',n, sep=' : ')
                            if not self.marked[n]:
                                ci_successor = n
                            else:
                                if ci_successor is not None:
                                    break
                    else:
                        ci_successor = self.ext_circle[ind - 1]  # ci_successor is the predecessor of ci on the
                        # external cycle. It is the vertex that will follow ci in neighbors(vk)
                    if ind == j:
                        print('ENT')
                        vk_successor = None
                        for it in range(self.g.degree(ci) - 1, -1, -1):
                            n = self.g.neighbors(ci)[it]
                            if not self.marked[n]:
                                vk_successor = n
                            else:
                                if vk_successor is not None:
                                    break
                    else:
                        vk_successor = self.ext_circle[ind + 1]
                    self.g.add_dummy_edge(vk, ci, ci_successor, vk_successor)
                    # neighbors_marked[ci] += 1
                    # if self.marked[ci]:
                    #     neighbors_marked[vk] += 1
                    # print('Neighbors after add edge ', vk, self.g.neighbors(vk), ci, self.g.neighbors(ci))

            self.ext_circle = self.ext_circle[:i + 1] + [vk] + self.ext_circle[j:]
            cl = self.rightup(i)
            cr = self.leftup(i + 2)

            if old[vk] == self.g.degree(vk):
                if cl is not None and cl == cr:
                    visit[cl] += 1
            else:
                if cl is not None and cl == self.leftup(i + 1):
                    visit[cl] += 1
                if cr is not None and cr == self.rightup(i + 1):
                    visit[cr] += 1

            if cl is not None and old[cl] == visit[cl] + 1:
                add_to_list(cl, readylist)
            if cr is not None and old[cr] == visit[cr] + 1:
                add_to_list(cr, readylist)

            self.marked[vk] = True

    def rightup(self, v_index: int) -> int:
        neighbor = self.ext_circle[(v_index + 1) % len(self.ext_circle)]
        v = self.ext_circle[v_index]
        index = self.g.neighbors(v).index(neighbor)
        rightup = self.g.neighbors(v)[index - 1]
        if self.marked[rightup]:
            return None
        return rightup

    def leftup(self, v_index: int) -> int:
        neighbor = self.ext_circle[v_index - 1]
        v = self.ext_circle[v_index]
        index = self.g.neighbors(v).index(neighbor)
        leftup = self.g.neighbors(v)[(index + 1) % self.g.degree(v)]
        if self.marked[leftup]:
            return None
        return leftup

    def left_and_right_vertices(self, x):
        """
        Let w1, w2, ..., wn the list of the vertex on the external circle, in the clockwise order (v1 is w1 and w2 is
        wn. x is out of this circle. Leftvertex (rightvertex) is wi, where i is minimal (resp. maximal), such that wi is
        a neighbor of x.
        :param x:
        :return: The indices of the leftvertex and rightvertex on the external circle (self.ext_circle)
        """
        left = None
        right = None
        for i in range(len(self.ext_circle)):
            if self.ext_circle[i] in self.g.neighbors(x):
                if left is None:
                    left = i
                right = i
            else:
                if left is not None:
                    break
        return left, right
