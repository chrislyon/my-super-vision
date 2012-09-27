import matplotlib as mpl
mpl.use('Agg')

import matplotlib.pyplot as plt
import numpy as np

val = ( 10, 30, 20, 50,10 )
pos = np.arange(len(val))+.5

plt.barh(pos , val , align='center' )  # on utilise la fonction sinus de Numpy

# Les Ticks
plt.yticks( pos, ( "DEMO_IDX", "DEMO_DAT", "TOTO_DAT", "TOTO_IDX", "USERS" ) )
plt.xticks (np.arange(0,101,25), ("0%", "25%", "50%", "75%") )

## Les Label 
plt.ylabel('TableSpace')
plt.xlabel("% Pourcentage Occupation")

plt.grid(True)


plt.savefig("toto.png", format="png")



