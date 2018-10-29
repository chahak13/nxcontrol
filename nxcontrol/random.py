import networkx
import itertools
import random

def randER(n, p, seed = None):
    G = networkx.DiGraph()
    G.add_nodes_from(range(1, n+1))

    if p<=0:
        return G
    elif p>=1:
        return networkx.complete_graph(n, create_using=G)

    if seed is not None:
        random.seed(seed)

    edge_list = itertools.permutations(range(1, n+1), 2)

    for u, v in edge_list:
        if random.random() > p:
            G.add_edge(u, v)
    
    return G