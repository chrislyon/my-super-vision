import matplotlib as mpl
mpl.use('Agg')

import matplotlib.pyplot as plt
import numpy as np

import pdb

def autolabel(rects):
	# attach some text labels
	for rect in rects:
		if rect.get_width() > 80:
			rect.set_color('#FF3333')
		else:
			rect.set_color('#99FF00')
			

val = ( 10, 30, 20, 90,10 )
pos = np.arange(len(val))+.5

r = plt.barh(pos , val , align='center' )  # on utilise la fonction sinus de Numpy

# Les Ticks
plt.yticks( pos, ( "DEMO_IDX", "DEMO_DAT", "TOTO_DAT", "TOTO_IDX", "USERS" ) )
plt.xticks (np.arange(0,101,25), ("0%", "25%", "50%", "75%") )

## Les Label 
plt.ylabel('TableSpace')
plt.xlabel("% Pourcentage Occupation")

plt.grid(True)

autolabel(r)

for p in np.arange(len(val)):
	plt.text( r[p].get_width()-5, p+0.5, "%d" % r[p].get_width(), fontsize=14 )


plt.savefig("toto.png", format="png")

