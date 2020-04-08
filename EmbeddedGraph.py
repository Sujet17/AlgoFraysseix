from nonOrientedGraph import Graph


class EmbeddedGraph(Graph):
    def __init__(self, g: Graph):
        if type(g) == Graph:
            Graph.__init__(self, g.size)
            self.embed(g)
        else:
            Graph.__init__(self, g)

    def add_edge(self, u, v):
        self.edgesCnt += 1
        self.edges[u].append(v)

    def embed(self, g):
        pass

    """
    def neighbors_between2(self, u, b1, b2):
        

        :param u:
        :param b1:
        :param b2:
        :return: The neighbors of u that are between b1 and b2 (both included)
       
        neighbors = self.neighbors(u)
        s = neighbors.index(b1)
        t = (neighbors.index(b2) + 1) % len(neighbors)

        if s < t:
            return neighbors[s:t]
        else:
            return neighbors[s:] + neighbors[:t]
    
    def neighbors_between(self, u, b1, b2, excluded_v):
        neighbors = self.neighbors(u)
        print(u, " : ",neighbors)
        s = neighbors.index(b1)
        t = (neighbors.index(b2) + 1) % len(neighbors)

        if s < t:
            if excluded_v in neighbors[s:t]:
                res = neighbors[t:] + neighbors[:s]
                res.reverse()
                return res
            else:
                return neighbors[s:t]

        else:
            if excluded_v in neighbors[s:] + neighbors[:t]:
                res = neighbors[t:s]
                res.reverse()
                return res
            else:
                return neighbors[s:] + neighbors[:t]
    """
