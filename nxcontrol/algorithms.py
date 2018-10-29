import networkx

def bipartite_unroll(G):
    B = nx.DiGraph()

    B.add_nodes_from(G.nodes(), bipartite=0)
    B.add_nodes_from([-1*node for node in G.nodes()], bipartite=1)
    bipartite_edges = [(e[0], -1*e[1]) for e in G.edges()]
    B.add_edges_from(bipartite_edges)
    
    return B

def max_matching_driver_nodes(G):
    B = bipartite_unroll(G)
    left_nodes = set(n for n,d in B.nodes(data=True) if d['bipartite']==0)
    hp = HopcroftKarp(B, left_nodes)
    matching = hp.match()
    # all unmatched nodes on right are drivers
    driver_nodes = set(-x for x in matching.keys() if matching[x] is None and x<0)
    return driver_nodes

def hopcroft_karp_matching(G, left_nodes):
    INFINITY = -1
    
