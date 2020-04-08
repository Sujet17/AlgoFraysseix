
class Graph:
    def __init__(self, size):
        self.size = size
        self.edges = [[] for i in range(size)]
        self.edgesCnt = 0
        
    def add_edge(self, u, v):
        self.edgesCnt += 1
        self.edges[u].append(v)
        self.edges[v].append(u)
        
    def is_edge(self, u, v):
        return v in self.edges[u]
        
    def neighbors(self, v):
        return self.edges[v]
