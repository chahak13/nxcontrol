import networkx as nx
from hopkroftKarp import HopcroftKarp

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

def maximum_matching_all_driver_nodes(G):
    '''
    Returns the set of driver nodes that are identified by a maximal matching using the Hopcroft-Karp Algorithm.
    '''
    # Unroll the given directed graph into a bipartite graph
    B = bipartite_unroll(G)
    left_nodes = set(n for n,d in B.nodes(data=True) if d['bipartite']==0)
    hp = HopcroftKarp(B, left_nodes)

    driverNodes, all_driver_nodes = hp.match_all()
    return driverNodes, all_driver_nodes

def minimum_dominating_set(G, start_with=None):
    all_nodes = set(G)
    if start_with is None:
        v = set(G).pop() # pick a node
    else:
        if start_with not in G:
            raise nx.NetworkXError('node %s not in G' % start_with)
        v = start_with
    D = set([v])
    ND = set(G[v])
    other = all_nodes - ND - D
    while other:
        w = other.pop()
        D.add(w)
        ND.update([nbr for nbr in G[w] if nbr not in D])
        other = all_nodes - ND - D
    return D