
# coding: utf-8

import networkx as nx
# import matplotlib.pyplot as plt
from modules import maximum_matching_driver_nodes, RandER
import time

g = nx.relabel_nodes(nx.read_edgelist('graph4.txt', create_using=nx.DiGraph), int)
print(nx.info(g))

# pos = nx.layout.spring_layout(g)
# nx.draw_networkx_nodes(g, pos, nodelist=g.nodes(), node_color='#EEEEEE')
# nx.draw_networkx_edges(g, pos, width=1.0, alpha=0.5)

print(g.nodes())

# take g and convert to bipartite graph
print("Via Networkx")
B = nx.DiGraph()
B.add_nodes_from(g.nodes(), bipartite=0)
B.add_nodes_from([-1*node for node in g.nodes()], bipartite=1)

bipartite_edges = [(e[0], -1*e[1]) for e in g.edges()]
B.add_edges_from(bipartite_edges)


top_nodes = set(n for n,d in B.nodes(data=True) if d['bipartite']==0)
bottom_nodes = set(B) - top_nodes
start_time = time.process_time()
matching = nx.algorithms.bipartite.matching.hopcroft_karp_matching(B, top_nodes = top_nodes)
end_time = time.process_time()
print(matching)
print("Networkx time: {}".format(end_time-start_time))
nonDriverNodes = set([-x for x in matching.keys() if x<0])
driverNodes = set(g.nodes())-nonDriverNodes

print(driverNodes)

print("Via code")
start_time = time.process_time()
d_nodes = maximum_matching_driver_nodes(g)
end_time = time.process_time()
print(d_nodes)
print("Networkx time: {}".format(end_time-start_time))

a = RandER(100, 0.5, seed=5)
print(nx.info(a))
