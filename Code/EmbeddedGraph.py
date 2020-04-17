from nonOrientedGraph import Graph


class EmbeddedGraph(Graph):
    def __init__(self, g: Graph):
        if type(g) == Graph:
            Graph.__init__(self, g.size)
            self.embed(g)
        else:
            Graph.__init__(self, g)
        self.dummy_edges = {}

    def add_edge(self, u, v):
        """
        Add v to the neighbors of u, at the end of the existing list of neighbors
        :param u:
        :param v:
        :return:
        """
        self.edgesCnt += 1
        self.edges[u].append(v)

    def add_dummy_edge(self, u: int, v: int, v_successor: int, u_successor: int):
        """

        :param u:
        :param v:
        :param v_successor: The vertex that follows v in the list of neighbors of u
        :param u_successor: The vertex that follows u in the list of neighbors of v
        :return:
        """
        if v not in self.edges[u]:
            print('dummy edge added', u, '<->', v)
            self.add_neighbor_after(u, v, v_successor)
            self.add_neighbor_after(v, u, u_successor)
            if u < v:
                self.dummy_edges[(u, v)] = True
            else:
                self.dummy_edges[(v, u)] = True

    def add_neighbor_after(self, u, v, v_successor):
        neighbors = self.neighbors(u)
        for i in range(len(neighbors)):
            n = neighbors[i]
            if n == v_successor:
                neighbors.insert(i, v)
                break

    def is_dummy_edge(self, u: int, v: int):
        if u < v:
            return self.dummy_edges.get((u, v), False)
        return self.dummy_edges.get((v, u), False)

    def embed(self, g):
        pass
