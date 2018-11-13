from modules import maximum_matching_driver_nodes, minimum_dominating_set

import networkx as nx

import ndlib.models.epidemics.SIModel as si
import ndlib.models.ModelConfig as mc

import time
import numpy as np
from ndlib.viz.mpl.DiffusionTrend import DiffusionTrend
import matplotlib.pyplot as plt

'''
returns top k hubs in a digraph (by out-degree)
'''
def top_hubs(g, k):
    degree_list = sorted(list(g.out_degree()), key=lambda x : x[1], reverse=True)[:k]
    return [x[0] for x in degree_list]

'''
returns an si model configured by the given parameters
'''
def SI_Model_Wrapper(graph=None, beta = 0.01, infected = []):
    # Model Selection
    model = si.SIModel(graph)

    #Initial configuration
    config = mc.Configuration()
    config.add_model_parameter('beta', beta)
    config.add_model_initial_configuration("Infected", infected)

    model.set_initial_status(config)

    return model

#load graph
g = nx.relabel_nodes(nx.read_edgelist('experiment_slashdot.txt', create_using=nx.DiGraph), int)

print('graph loaded')

# driver nodes
d_nodes = maximum_matching_driver_nodes(g)
print('found driver nodes')
n_driver = len(d_nodes)

# top hubs
hubs = top_hubs(g, n_driver)

model_driver = SI_Model_Wrapper(graph = g, beta = 0.005, infected = d_nodes)
model_hubs = SI_Model_Wrapper(graph = g, beta = 0.005, infected = hubs)

print('starting SI for drivers')
iterations_driver = model_driver.iteration_bunch(1000)
trends_driver = model_driver.build_trends(iterations_driver)

print('starting SI for hubs')
iterations_hubs = model_hubs.iteration_bunch(1000)
trends_hubs = model_hubs.build_trends(iterations_hubs)

I_driver = np.array(trends_driver[0]['trends']['node_count'][1])/g.number_of_nodes()
I_hubs = np.array(trends_hubs[0]['trends']['node_count'][1])/g.number_of_nodes()

np.save('I_driver.npy', I_driver)
np.save('I_hubs.npy', I_hubs)

plt.plot(I_driver, "k")
plt.plot(I_hubs, "r")
plt.grid(True)
plt.xlabel(r'iterations')
plt.ylabel(r'$\frac{I}{N}$')

plt.savefig("plot.png", format = "png", dpi = 300)

degree_driver = np.array([x[1] for x in list(g.out_degree(d_nodes))])
degree_hubs = np.array([x[1] for x in list(g.out_degree(hubs))])

np.save('degree_driver.npy', degree_driver)
np.save('degree_hubs.npy', degree_hubs)