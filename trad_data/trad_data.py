## ------------
## Trad_data
## ------------

import os, sys
import pprint
        
import pdb

## --------------------------------
## Generation de Restructured Text
## --------------------------------
def gnr_rst(cles, data):
	for cle in cles:
		t = eval(cle)
		#print len(t), cle, t
		l = len(t)
		tabs = ' ' * (l-1)
		if l == 1:
			print tabs,
			print "Entete du fichier"

		## Serveur / Database
		if l == 2:
			print tabs,
			print "Chapitre : %s " % t[1]

		## Sections
		## Si serveur
		## Desc et Disk
		## Si database
		## Alors Nom de la database
		if l == 3:
			if t[1] == "SERVEURS":
				if t[2] == "SERVEUR_DESC":
					t[2] = "Description du serveur"
				if t[2] == "SERVEUR_DF":
					t[2] = "Ressources Disques"

			print tabs,
			print "Sections : %s " % t[2]

		## Databases
		## BIG_Table / DB_CACHE / TBS
		if l == 4:
			print tabs,
			print "SubSections : %s " % t[3]

		## Big_Table => Appli
		## DB_CACHE => Donnees
		## TBS => Donnees
		if l == 5:
			if t[4].startswith('REQUETE'):
				continue

			if t[3] == "BIG_TABLE":
				t[4] = " User / Application : %s " % t[4]
			print tabs,
			print "S-SubSections : %s " % t[4]

		## Big_Table => Appli => Donnees
		if l == 6:
			if t[5].startswith('REQUETE'):
				continue

			print tabs,
			print "S-S-SubSections : %s " % t[5]
			


## -------------------
## Calcul de la cle
## -------------------
def trad_cle(s):
    t = s.split(':')[1]
    c = t.split('-')[0]
    return c

## -----------------------
## Lecture du fichier
## -----------------------
def lire(fichier):
	ENT_CHAPITRE = '#>>>'
	DEB_CHAP = "-DEB:#"
	FIN_CHAP = "-FIN:#"
	chap = {}
	cle = []
	all_cle = []
	for l in open(fichier, 'r').readlines():
		l  = l.strip()
		if l.startswith(ENT_CHAPITRE):
			if l.endswith(DEB_CHAP):
				c = trad_cle(l)
				cle.append(c)
				chap[str(cle)] = []
				all_cle.append(str(cle))
			elif l.endswith(FIN_CHAP):
				cle.pop()
		else:
			chap[str(cle)].append(l)
	return all_cle, chap


if __name__ == '__main__':
	if len(sys.argv) > 1:
		if os.path.exists(sys.argv[1]):
			pp = pprint.PrettyPrinter(indent=4)
			cles, data = lire(sys.argv[1])
			#print pp.pprint(data)
			#print pp.pprint(cles)
			gnr_rst(cles, data)
		else:
			print "Fichier inexistant %s " % sys.argv[1]
