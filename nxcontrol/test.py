import networkx as nx
import matplotlib.pyplot as plt
from algorithms import maximum_matching_driver_nodes, maximum_matching_all_driver_nodes, minimum_dominating_set
from randomGraphs import rand_gnm_directed, rand_gnm_undirected, randER_directed, randER_fast_directed, randER_fast_undirected, randER_undirected
import time
import numpy as np
import argparse
from tqdm import tqdm
from networkx.algorithms.community import greedy_modularity_communities
from pprint import pprint
import sys

sys.setrecursionlimit(100000)

def test_all_maximum_matching(g):
    start_time = time.process_time()
    d_nodes, all_d_nodes = maximum_matching_all_driver_nodes(g)
    end_time = time.process_time()
    print("Driver nodes: {}".format((d_nodes)))
    print("Potential driver nodes: {}".format((all_d_nodes)))
    print("Fraction of potential driver nodes: {:.4f}".format(len(all_d_nodes)/len(g)))
    print("Time taken: {:.5f}".format(end_time - start_time))
    return

def test_maximum_matching(g):
    start_time = time.process_time()
    d_nodes = maximum_matching_driver_nodes(g)
    end_time = time.process_time()
    print((d_nodes))
    print("Code time: {}".format(end_time-start_time))

def test_randER(n=100, p=0.1, seed=5):
    start_time = time.process_time()
    a = randER_directed(n, p, seed=seed)
    end_time = time.process_time()
    print(nx.info(a))
    print("Time taken to create graph: {}".format(end_time-start_time))
    return

def test_randER_fast(n=100, p=0.1, seed=5):
    start_time = time.process_time()
    b = randER_fast_directed(n, p, seed=seed)
    end_time = time.process_time()
    print(nx.info(b))
    print("Time taken to create graph: {}".format(end_time-start_time))
    return

def test_minimum_dominating_set(G):
    dominating_set = minimum_dominating_set(G)
    print(dominating_set)
    print(len(dominating_set))
    return

def test_rand_gnm(n,m):
    g = rand_gnm_undirected(n,m)
    print(nx.info(g))
    return g

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--file', required=False, type=str, help="File that contains edgelist of graph to be loaded.")
    args = parser.parse_args()

    g = nx.relabel_nodes(nx.read_edgelist('./graphs/'+args.file+'.txt', create_using=nx.DiGraph), int)
    # print("="*35)
    # print("Loaded graph")
    # print(nx.info(g))
    print("="*35)
    print("Driver nodes")
    test_maximum_matching(g)
    print("="*35)
    print("All possible driver nodes")
    # test_all_maximum_matching(g)
    # print("="*35)
    # print("Random ER graph generation")
    # test_randER(n = 100, p = 0.2, seed = 5)
    # print("="*35)
    # print("Fast random ER graph generation")
    # test_randER_fast(n = 688, p = 0.002282844, seed = 5)
    # print("="*35)
    # print("Minimum Dominating Set")
    test_minimum_dominating_set(g)
