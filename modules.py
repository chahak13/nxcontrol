#Algorithms for bipartite graphs

import networkx as nx
import collections
import random
import itertools
import math

def randER(n, p, seed = None):
    '''
    Creates a random graph with n nodes and p probability of two vertices being connected.
    (Currently works in O(n^2))
    '''
    G = nx.DiGraph()
    G.name = "randER({n}, {p}, {seed})".format(n=n, p=p, seed=seed)
    G.add_nodes_from(range(1, n+1))

    if p <= 0:
        return G
    elif p >=1:
        return nx.complete_graph(n, create_using = nx.DiGraph)

    if seed is not None:
        random.seed(seed)

    edge_list = itertools.permutations(range(1, n+1), 2)

    for u, v in edge_list:
        if random.random() < p:
            G.add_edge(u, v)

    return G

def randER_fast(n, p, seed = None):
    '''
    A faster version of randER. Works in O(n+m) thereby solving the scalability issue of randER.
    '''
    G = nx.DiGraph()
    G.name = "randER_fast({n}, {p}, {seed})".format(n=n, p=p, seed=seed)
    G.add_nodes_from(range(1, n+1))

    if p <= 0:
        return G
    elif p >=1:
        return nx.complete_graph(n, create_using = nx.DiGraph)

    if seed is not None:
        random.seed(seed)

    if n<50:
        return randER(n, p, seed)
    else:
        v, w = 1,0
        while v<=n:
            r = random.random()
            w = w + 1 + math.floor((math.log(1-r)/math.log(1-p)))
            if v==w:
                w += 1
            while w >= n and v <= n:
                w = w - n + 1
                v += 1
                if v==w:
                    w += 1
            if v <= n:
                G.add_edge(int(v), int(w))
        return G

def maximum_matching_driver_nodes(G):
    '''
    Returns the set of driver nodes that are identified by a maximal matching using the Hopcroft-Karp Algorithm.
    '''
    # Unroll the given directed graph into a bipartite graph
    B = nx.DiGraph()
    B.add_nodes_from(G.nodes(), bipartite=0)
    B.add_nodes_from([-1*node for node in G.nodes()], bipartite=1)

    bipartite_edges = [(e[0], -1*e[1]) for e in G.edges()]
    B.add_edges_from(bipartite_edges)

    # Calculate the driver nodes using maximum matching via HopcroftKarp
    top_nodes = set(n for n,d in B.nodes(data=True) if d['bipartite']==0)
    hp = HopcroftKarp(B, top_nodes)
    matching = hp.match()
    driverNodes = set(-x for x in matching.keys() if matching[x] is None and x<0)

    return driverNodes

class HopcroftKarp(object):
    INFINITY = -1

    def __init__(self, G, top_nodes):
        self.G = G
        self.top_nodes = top_nodes

    def match(self):
        self.N1 = self.top_nodes
        self.N2 = set(self.G.nodes) - self.top_nodes
        self.pair = {}
        self.dist = {}
        self.q = collections.deque()

        #init
        for v in self.G:
            self.pair[v] = None
            self.dist[v] = HopcroftKarp.INFINITY

        matching = 0

        while self.bfs():
            for v in self.N1:
                if self.pair[v] is None and self.dfs(v):
                    matching = matching + 1

        # print("Pair: ", self.pair)
        return self.pair

    def dfs(self, v):
        if v != None:
            for u in self.G.neighbors(v):
                if self.dist[ self.pair[u] ] == self.dist[v] + 1 and self.dfs(self.pair[u]):
                    self.pair[u] = v
                    self.pair[v] = u

                    return True

            self.dist[v] = HopcroftKarp.INFINITY
            return False

        return True

    def bfs(self):
        for v in self.N1:
            if self.pair[v] == None:
                self.dist[v] = 0
                self.q.append(v)
            else:
                self.dist[v] = HopcroftKarp.INFINITY

        self.dist[None] = HopcroftKarp.INFINITY

        while len(self.q) > 0:
            v = self.q.popleft()
            if v != None:
                for u in self.G.neighbors(v):
                    if self.dist[ self.pair[u] ] == HopcroftKarp.INFINITY:
                        self.dist[ self.pair[u] ] = self.dist[v] + 1
                        self.q.append(self.pair[u])

        return self.dist[None] != HopcroftKarp.INFINITY
