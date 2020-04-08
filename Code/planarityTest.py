import random


# Not tested yet
class DFS:
    def __init__(self, g):
        self.g = g
        self.tree = []
        self.cnt = 1
        self.dfn = [-1] * g.size
        self.low = [-1] * g.size
        self.fathers = [-1] * g.size
        self.marks = ['new'] * g.size

    def get_ordering(self):
        # v = random.randrange(self.g.size)
        self.search(0)
        return self.tree, self.low, self.fathers, self.dfn

    def search(self, v):
        self.marks[v] = 'old'
        self.dfn[v] = self.cnt
        self.cnt += 1
        self.low[v] = self.dfn[v]
        for w in self.g.neighbors(v):
            if self.marks[w] == 'new':
                self.tree.append((v, w))
                self.fathers[w] = v
                self.search(w)
                self.low[v] = min(self.low[v], self.low[w])
            elif w != self.fathers[v]:
                self.low[v] = min(self.low[v], self.dfn[w])


class Path:
    def __init__(self, g):
        self.path = []
        self.g = g

    def path(self, v):
        old_edges = []
        for w in self.g.neighbors(v):
            if (v, w) in old_edges:
                self.path.append((v, w))
                old_edges.append((v, w))
        pass


def st_number(g, s=1, t=0):
    vertex_mark = ['new'] * g.size
    edges_mark = {}
    S = []
    vertex_mark[s] = 'old'
    vertex_mark[t] = 'old'
    edges_mark[(t, s)] = True
    S.append(t)
    S.append(s)
    cnt = 1
    path = Path(g)
    stn = [None] * g.size

    v = S.pop()
    while v != t:
        path_v = path.path(v)
        if len(path_v) == 0:
            stn[v] = cnt
            cnt += 1
        else:
            for s in reversed(path_v[:-1]):
                S.append(s)
        v = S.pop()
    stn[t] = cnt
    return stn
