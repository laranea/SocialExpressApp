import numpy as np

x = [1, 2, 3, 4, 5, 6, 7]
y = [1, 2, 1, 2, 3, 2, 1]
b = (np.diff(np.sign(np.diff(y))) > 0).nonzero()[0] + 1 # local min
c = (np.diff(np.sign(np.diff(y))) < 0).nonzero()[0] + 1 # local max
xmins = [x[i] for i in b]
ymins = [y[i] for i in b]
xmaxs = [x[i] for i in c]
ymaxs = [y[i] for i in c]

print xmins
print ymaxs