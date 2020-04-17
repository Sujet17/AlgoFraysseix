
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

    def degree(self, v):
        return len(self.edges[v])

    def sum_degrees(self):
        return sum([self.degree(i) for i in range(self.size)])

    def __str__(self):
        result = ""
        for i in range(self.size):
            result += str(self.edges[i]) + "\n"
        return result
