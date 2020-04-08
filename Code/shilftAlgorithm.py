from EmbeddedGraph import EmbeddedGraph


class ShiftAlgorithm:
    def __init__(self, g, ordering):
        self.g = g
        self.ordering = ordering
        self.v1, self.v2, self.v3 = ordering[:3]

        self.left = ['N'] * g.size
        self.right = ['N'] * g.size
        self.offset = [None] * g.size
        self.y = [None] * g.size

        self.offset[self.v1] = 0
        self.y[self.v1] = 0
        self.right[self.v1] = self.v3
        self.left[self.v1] = None
        self.offset[self.v3] = 1
        self.y[self.v3] = 1
        self.right[self.v3] = self.v2
        self.left[self.v3] = None
        self.offset[self.v2] = 1
        self.y[self.v2] = 0
        self.right[self.v2] = None
        self.left[self.v2] = None

    def run(self):
        self.phase1()
        # print(self.left)
        # print(self.right)
        self.accumulate_offset(self.v1, 0)
        return self.offset, self.y

    def phase1(self):
        for k in range(3, self.g.size):
            # wi = get_outer_cycle(g)
            wi = []
            vk = self.ordering[k]
            neighbors_wi = self.find_neighbors_wi(vk)
            # print(k, vk, self.left, '\n', self.right, '\n', 'neighbors :', neighbors_wi, sep=' ; ')
            wp = neighbors_wi[0]
            wq = neighbors_wi[-1]
            self.offset[neighbors_wi[1]] += 1
            self.offset[wq] += 1
            offset = self.sum_offsets(neighbors_wi)
            self.offset[vk] = 0.5 * (offset - self.y[wp] + self.y[wq])
            self.y[vk] = 0.5 * (offset + self.y[wp] + self.y[wq])
            self.offset[wq] = offset - self.offset[vk]

            if len(neighbors_wi) > 2:
                self.offset[neighbors_wi[1]] -= self.offset[vk]
            self.right[wp] = vk
            self.right[vk] = wq

            if len(neighbors_wi) > 2:
                self.left[vk] = neighbors_wi[1]
                self.right[neighbors_wi[-2]] = None
            else:
                self.left[vk] = None

    def sum_offsets(self, neighbors_wi):
        return sum([self.offset[i] for i in neighbors_wi[1:]])

    def accumulate_offset(self, v, delta):
        if v is not None:
            self.offset[v] += delta
            self.accumulate_offset(self.left[v], self.offset[v])
            self.accumulate_offset(self.right[v], self.offset[v])

    def find_neighbors_wi(self, vk):
        neighbors = self.g.neighbors(vk)
        wp_index = None
        wq_index = None
        for i in range(len(neighbors)):
            n = neighbors[i]
            if self.placed(n) and not self.placed(neighbors[(i + 1) % len(neighbors)]):
                wq_index = i
            elif self.placed(n) and not self.placed(neighbors[i - 1]):
                wp_index = i

        # print(wp_index, wq_index)
        # print(neighbors)
        if wp_index is None:
            assert wq_index is None
            wpq = neighbors[:]
        else:
            wq_index = (wq_index + 1) % len(neighbors)
            if wp_index < wq_index:
                wpq = neighbors[wp_index:wq_index]
            else:
                wpq = neighbors[wp_index:] + neighbors[:wq_index]

        # print(wpq)
        wpq.reverse()
        return wpq

    def placed(self, v):
        return self.right[v] != 'N'


def union(*lists):
    r = []
    for l in lists:
        r += l
    return l


class NaiveShiftAlgorithm:
    def __init__(self, g: EmbeddedGraph, ordering: list):
        self.y = [None] * g.size
        self.x = [None] * g.size
        v1, v2, v3 = ordering[:3]
        L = [[v1], [v3], [v2]]
        wi = [v1, v3, v2]
        for vk in ordering[3:]:
            wpq = update_wi(g, wi, vk)
            wp, wq = wpq[0], wpq[-1]

    def mu(self, wp, wq):
        x1, y1 = self.x[wp], self.y[wp]
        x2, y2 = self.x[wq], self.y[wq]
        return (x1 - y1 + y2 + x2) * 0.5, (y1 - x1 + y2 + x2) * 0.5


def update_wi(g, wi, x):
    for i in range(len(wi)):
        if wi[i] == x:
            wq = wi[(i + 1) % len(wi)]
            wp = wi[i - 1]
            wi.pop(i)
            wpq = g.neighbors_between2(x, wq, wp)
            wpq.reverse()
            for n in g.neighbors_between2(x, wq, wp)[1:-1]:
                wi.insert(i, n)
            return wpq
            break
