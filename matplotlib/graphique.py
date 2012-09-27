import matplotlib as mpl
mpl.use('Agg')

import matplotlib.pyplot as plt
import numpy as np

import pdb

def tbs_graph( data=[], noms=[], fichier="tbs_graph.png", format="png" ):
	
	nb = len(data)

	pos = np.arange(nb)+.5

	r = plt.barh(pos , data , align='center' )

	# Les Ticks
	plt.yticks( pos, []  )
	plt.xticks (np.arange(0,101,25), ("  ", "25%", "50%", "75%", "100%" ) )

	## Les Label 
	plt.ylabel('TableSpaces')
	plt.xlabel("% Pourcentage Occupation")

	## Titre et grille
	plt.title(" Taux d'occupation des tablespaces en %")
	plt.grid(True)

	## Quelques ajustements
	for p in np.arange(nb):
			d = r[p].get_height()/2
			plt.text( 5, p+d-0.2, "%s : %d %%" % (noms[p], r[p].get_width()), fontsize=12 )

	for p in r:
		if p.get_width() > 80:
			p.set_color('#FF3333')
		else:
			p.set_color('#99FF00')
		
	## Sauvegarde du fichier
	if not fichier.endswith(format):
		fichier += '.'+format

	plt.savefig( fichier, format="png")


if __name__ == '__main__':
	nom_tbs = ( "DEMO_IDX", "DEMO_DAT", "TOTO_DAT", "TOTO_IDX", "SUPER_LONG_TABLESPACE", "USERS" )
	tbs_occ = ( 10, 30, 20, 2, 50,10 )
	tbs_graph( data = tbs_occ, noms = nom_tbs, fichier = "TBS_OCC", format='png' )
