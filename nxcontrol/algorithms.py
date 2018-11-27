import networkx as nx
from hopcroftKarp import HopcroftKarp

def bipartite_unroll(G):
    """Returns bipartite projection of a directed graph ``G``.

    Returns
    -------
    B : Networkx bipartite graph

    The graph ``G`` is unrolled into an undirected bipartite network with nodes of ``G`` on both sides of the bipartite. There is an edge from ``u`` in the left side to ``v`` in the right side if there is an edge from ``u`` to ``v`` in the graph ``G``.
    """
    B = nx.Graph()

    B.add_nodes_from(G.nodes(), bipartite=0)
    B.add_nodes_from([-1*node for node in G.nodes()], bipartite=1)
    bipartite_edges = [(e[0], -1*e[1]) for e in G.edges()]
    B.add_edges_from(bipartite_edges)
    
    return B

def maximum_matching_driver_nodes(G):
    """Returns the driver nodes determined by using maximal matching by Hopcroft-Karp Algorithm.

    Returns
    -------
    driver_nodes : set

    The set ``driver_nodes`` is determined by using maximal matching as said by Liu et al. The driver nodes are determined by the unmatched nodes on the right hand side of the maximal matching bipartite partition.

    References
    ----------
    .. [1] Liu, Yang-Yu & Slotine, Jean-Jacques & Barabasi, Albert-Laszlo.  (2011).  Controllability
of complex networks.  Nature.  473.  167-73.  <https://dx.doi.org/10.1038/nature10011>.
    """
    B = bipartite_unroll(G)
    left_nodes = set(n for n,d in B.nodes(data=True) if d['bipartite']==0)
    hp = HopcroftKarp(B, left_nodes)
    matching = hp.match()
    # all unmatched nodes on right are drivers
    driver_nodes = set(-x for x in matching.keys() if matching[x] is None and x<0)
    if len(driver_nodes) == 0:
        driver_nodes.add(list(G.nodes())[0])
    return driver_nodes

def maximum_matching_all_driver_nodes(G):
    """Returns maximal matching using the Hopcroft-Karp Algorithm, set of driver nodes and set of all possible driver node for the graph `G`.

    Returns
    -------
    driver_nodes : set

    Set of nodes that are the driver nodes for graph `G`. They are determined by finding the unmatched nodes in the right side of the Hopcroft-Karp matching. 

    all_driver_nodes : set

    Set of nodes such that all nodes are possible driver nodes in different maximal matchings for graph `G`. They are determined by finding the unmatched nodes in the right side of the Hopcroft-Karp matching and then applying DFS on them.

    References
    ----------
    .. [1]  Zhang, Xizhe & Han, Jianfei & Zhang, Weixiong.  (2017).  An efficient algorithm for finding all possible input nodes for controlling complex networks.  Scientific Reports.  7.  10677. <https://dx.doi.od10.1038/s41598-017-10744-w

    """
    # Unroll the given directed graph into a bipartite graph
    B = bipartite_unroll(G)
    left_nodes = set(n for n,d in B.nodes(data=True) if d['bipartite']==0)
    hp = HopcroftKarp(B, left_nodes)

    matching, driverNodes, all_driver_nodes = hp.match_all()
    if len(driverNodes) == 0:
        driverNodes.add(list(G.nodes())[0])
        all_driver_nodes.add(frozenset(G.nodes))
    return driverNodes, all_driver_nodes

def minimum_dominating_set(G, start_with=None):
    """Returns the driver nodes based on the idea of Minimum Dominating Set

    Returns
    -------

    D : set

    Set of driver nodes determined by using the Minimum Dominating Set algorithm.
    """
    if G.is_directed():
        G = G.to_undirected()
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