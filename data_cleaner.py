import numpy as np

data = np.loadtxt(open('yeastinter_st.txt', 'r'), dtype = int, usecols = (0, 1))
data += 1
np.savetxt("experiment_yeast.txt", data, fmt = "%d")
