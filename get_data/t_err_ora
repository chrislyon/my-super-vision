#! /usr/bin/env python
## ---------------------------------------------
## Extractions et formattage des errors Oracle
## ---------------------------------------------

import sys
import re
import pdb

class evenement(object):
    def __init__(self,n, date):
        self.vide = True
        self.date = date
        self.uniqid = n
        self.data = []

    def contient_erreur(self):
        for l in self.data:
            if l.startswith('ORA-') or l.startswith('Errors'):
                return True
        return False

    def add(self,ligne):
        self.data.append(ligne)
        self.vide = False

    def is_vide(self):
        return self.vide

    def pr(self):
        r = "%25s : No = %d\n" % ( self.date, self.uniqid)
        for l in self.data:
            r += "%25s : %s" % ("", l)
            r += "\n"
        return r

    def __str__(self):
        return self.pr()

def do_t_err(ora_log):

    p = re.compile(r"""
        ^                           # Au debut
        [A-Z][a-z][a-z]             # Jour
        \s*
        [A-Z][a-z][a-z]             # Mois
        \s*
        [0-9]{1,2}                  # Jour
        \s*
        [0-9]{2}:[0-9]{2}:[0-9]{2}  # Heure
        \s*
        [0-9]{4}                    # Annee
        \s*
        $                           # A la fin
        """, re.VERBOSE)

    evt = None 
    nb = 0

    for ligne in ora_log:
        nb += 1
        ligne = ligne.strip()
        result = p.match(ligne)
        ## Si c'est une Date
        if result:
            if evt and not evt.is_vide():
                # Si c'est pas vide on Traite
                do_the_work(evt)
            ## Dans tout les cas on cree un nouvel evenement
            evt = evenement(nb, ligne)
        ## Sinon on Ajoute
        else:
            evt.add(ligne)
    else:
        do_the_work(evt)

def do_the_work( evt ):
    if evt.date:
        if evt.contient_erreur():
            print evt
    else:
        print "Pas de date => %s " % evt

def usage():
    t = "\n"
    t += "usage: %s fichier_alert_SID.log\n" % sys.argv[0]
    t += "\t fichier = fichier alert d'une base oracle\n"
    t += "\n"
    print >> sys.stderr, t
    sys.exit(1)


if __name__ == "__main__":
    try:
        data = open(sys.argv[1], "r").readlines()
    except:
        usage()

    do_t_err(data)

