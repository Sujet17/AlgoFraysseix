import networkx as nx


class ShiftAlgorithm:
    def __init__(self, embedding: nx.PlanarEmbedding, ordering: list):
        self.embedding = embedding
        self.ordering = ordering
        self.v1, self.v2, self.v3 = [c[0] for c in ordering[:3]]

        self.left = ['N'] * len(embedding)
        self.right = ['N'] * len(embedding)
        self.offset = [None] * len(embedding)
        self.y = [None] * len(embedding)

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
        for k in range(3, len(self.embedding)):
            # wi = get_outer_cycle(g)
            wi = []
            vk, neighbors_wi = self.ordering[k]
            # neighbors_wi = self.find_neighbors_wi(vk)
            # print(k, vk, self.left, '\n', self.right, '\n', 'neighbors :', neighbors_wi, sep=' ; ')
            wp = neighbors_wi[0]
            wq = neighbors_wi[-1]
            self.offset[neighbors_wi[1]] += 1
            self.offset[wq] += 1
            offset = sum([self.offset[i] for i in neighbors_wi[1:]])
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

    def accumulate_offset(self, v, delta):
        if v is not None:
            self.offset[v] += delta
            self.accumulate_offset(self.left[v], self.offset[v])
            self.accumulate_offset(self.right[v], self.offset[v])

    def placed(self, v):
        return self.right[v] != 'N'
