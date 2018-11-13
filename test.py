
# coding: utf-8

import networkx as nx
# import matplotlib.pyplot as plt
from modules import maximum_matching_driver_nodes, randER, randER_fast, minimum_dominating_set
import time
import numpy as np
from tqdm import tqdm

def test_maximum_matching(g):
    print("Via Networkx")
    start_time = time.process_time()
    B = nx.DiGraph()
    B.add_nodes_from(g.nodes(), bipartite=0)
    B.add_nodes_from([-1*node for node in g.nodes()], bipartite=1)

    bipartite_edges = [(e[0], -1*e[1]) for e in g.edges()]
    B.add_edges_from(bipartite_edges)


    top_nodes = set(n for n,d in B.nodes(data=True) if d['bipartite']==0)
    bottom_nodes = set(B) - top_nodes
    matching = nx.algorithms.bipartite.matching.hopcroft_karp_matching(B, top_nodes = top_nodes)
    nonDriverNodes = set([-x for x in matching.keys() if x<0])
    driverNodes = set(g.nodes())-nonDriverNodes
    end_time = time.process_time()

    print(len(driverNodes))
    print("Networkx time: {}".format(end_time-start_time))

    print("Via code")
    start_time = time.process_time()
    d_nodes = maximum_matching_driver_nodes(g)
    end_time = time.process_time()
    print(len(d_nodes))
    print("Networkx time: {}".format(end_time-start_time))

def test_randER(n=100, p=0.1, seed=5):
    start_time = time.process_time()
    a = randER(n, p, seed=seed)
    end_time = time.process_time()
    print(nx.info(a))
    print("Time taken to create graph: {}".format(end_time-start_time))
    return

def test_randER_fast(n=100, p=0.1, seed=5):
    start_time = time.process_time()
    b = randER_fast(n, p, seed=seed)
    end_time = time.process_time()
    print(nx.info(b))
    print("Time taken to create graph: {}".format(end_time-start_time))
    return

def test_minimum_dominating_set(G):
    dominating_set = minimum_dominating_set(G)
    print(dominating_set)
    print(len(dominating_set))
    return

if __name__ == '__main__':

    g = nx.relabel_nodes(nx.read_edgelist('experiment_yeast.txt', create_using=nx.DiGraph), int)
    print(nx.info(g))

    # test_maximum_matching(g)
    # test_randER(n = 10000, p = 0.2, seed = 5)
    # test_randER_fast(n = 688, p = 0.002282844, seed = 5)

    # nodeFraction = []
    # for i in tqdm(range(100)):
    #     g = randER_fast(n = 688, p = 0.002282844)
    #     driverNodes = maximum_matching_driver_nodes(g)
    #     nodeFraction.append(len(driverNodes)/688.0)
    #
    # avg = np.mean(nodeFraction)
    # print(avg)
    test_minimum_dominating_set(g)
