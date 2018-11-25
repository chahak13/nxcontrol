class HopcroftKarp(object):
    INFINITY = -1

    def __init__(self, G, left_nodes):
        self.G = G
        self.left_nodes = left_nodes
        self.count = 0

    def match(self):
        self.N1 = self.left_nodes
        self.N2 = set(self.G.nodes) - self.left_nodes
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

    def match_all(self):
        self.N1 = self.left_nodes
        self.N2 = set(self.G.nodes) - self.left_nodes
        self.pair = {}
        self.dist = {}
        self.q = collections.deque()
        self.candidates = set()
        self.marked_nodes = []
        self.marked_edges = []

        #init
        for v in self.G:
            self.pair[v] = None
            self.dist[v] = HopcroftKarp.INFINITY

        matching = 0

        while self.bfs():
            for v in self.N1:
                if self.pair[v] is None and self.dfs(v, all=True):
                    matching = matching + 1

        current_nodes = set(-x for x in self.pair.keys() if self.pair[x] is None and x<0)
        self.candidates = self.candidates | set(-x for x in current_nodes)
        self.marked_edges = [(u, v) for u, v in self.pair.items() if v is not None]

        additional_nodes = set()
        for node in self.N2:
            if node in current_nodes:
                continue

        for node in current_nodes:
            self.dfs_path_search(-node, reset = True)
            additional_nodes = additional_nodes | set(-x for x in self.marked_nodes if x<0)

        all_driver_nodes = current_nodes | additional_nodes
        return self.pair, current_nodes, all_driver_nodes

    def dfs_path_search(self, v, prevMark = True, reset = False):

        if reset:
            self.marked_nodes = []

        if v!= None:
            for u in self.G.neighbors(v):
                if (((v, u) in self.marked_edges) != prevMark) and u not in self.marked_nodes:
                    self.marked_nodes.append(u)
                    self.dfs_path_search(u, prevMark = not prevMark)
        return

    def dfs(self, v, all=False):
        if v != None:
            for u in self.G.neighbors(v):
                if self.dist[ self.pair[u] ] == self.dist[v] + 1 and self.dfs(self.pair[u]):
                    self.pair[u] = v
                    self.pair[v] = u
                    if all and u < 0:
                        self.candidates.add(u)
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
