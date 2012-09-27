import matplotlib as mpl
mpl.use('Agg')

import matplotlib.pyplot as plt
import numpy as np

p1 = [ 10, 40, 50, 20 ]
p2 = [ 90, 60, 50, 80 ]

ind = np.arange(4)

width=1


plt.bar(ind, p1, width, color='lightblue' )
plt.bar(ind, p2, width, bottom=p1, color='red')

## Les Label 
plt.ylabel('Valeur Y')
plt.xlabel("Valeur X")


plt.savefig("toto.png", format="png")
