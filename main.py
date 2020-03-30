import matplotlib.pyplot as plt
import numpy as np

strings = ["abc","abc","abc","pqr","pqr","xyz"]
year = list(range(2012,2018))
avg = [1854, 2037,1781,1346,1667,1952]

u, ind = np.unique(strings, return_inverse=True)
plt.scatter(ind, year, s=avg)
plt.xticks(range(len(u)), u)

plt.show()