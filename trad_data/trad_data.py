## ------------
## Trad_data
## ------------

import os, sys
import pprint

import rtext as rst

import graphique as gr
        
import pdb

## --------------------------------
## Generation de Restructured Text
## --------------------------------
def gnr_rst(cles, data, mode=0 ):

    doc = None    # Doc courant 
    p = None    # Page courante

    for cle in cles:
        t = eval(cle)
        #print len(t), cle, t
        l = len(t)
        tabs = ' ' * (l-1)
        if l == 1:
            if mode == 1:
                print tabs,
                print "Entete du fichier"
            ## On cree 
            doc = rst.Fichier()
            doc.add(rst.Entete())

            p = rst.Page()
            p.add( rst.Contenu( "**DOSSIER : <NOM CLIENT>**" ) )
            p.add( rst.Contenu( "\n" ) )
            p.add( rst.Contenu( "**Sujet : Rapport du <DATE>**" ) )
            p.add( rst.Contenu( "\n" ) )
            p.add( rst.Contenu( "**Rapport d'etat du systeme**" ) )
            p.add( rst.Contenu( "\n" ) )
            p.add( rst.Saut_Page() )
            doc.add(p)


        ## Serveur / Database
        if l == 2:

            if mode == 1:
                print tabs,
                print "Chapitre : %s " % t[1]

            p = rst.Page()
            p.add(rst.Titre("Chapitre : %s : " % t[1]))
            doc.add(p)

            if t[1] == "ENT":
                p.add( rst.Contenu("Entete : %s " % data[cle] ))

        ## Sections
        ## Si serveur
        ## Desc et Disk
        ## Si database
        ## Alors Nom de la database
        if l == 3:
            p = rst.Page()
            section = ""
            if t[1] == "SERVEURS":
                if t[2] == "SERVEUR_DESC":
                    section = "Description du serveur"
                if t[2] == "SERVEUR_DF":
                    section = "Ressources Disques"

            p.add(rst.Section("Sections : %s : " % section ))
            if t[2] == "SERVEUR_DF":
                d = []
                d.append([ "File System", "Blocs de 1K", "Utilise", "Dispo", "% Occupe" ])
                #d.append([ "File SYstem", "Blocs de 1K", "Utilise", "Dispo", "% Occupe", "Monte sur" ])
                for l in data[cle][3:]:
                    d_tmp = l.split()
                    d.append(  [ d_tmp[5], d_tmp[1], d_tmp[2], d_tmp[3], d_tmp[4] ] )

                p.add(rst.Table(d))
                p.add( rst.Saut_Page() )

            ## Si 3 cles et DATABASES alors c'est le nom
            if t[1] == "DATABASES":
                p = rst.Page()
                p.add(rst.Section("Database : %s : " % t[2] ))

            if mode == 1:
                print tabs,
                print "Sections : %s " % section 
            ## On valide la page
            doc.add(p)


        ## Databases
        ## BIG_Table / DB_CACHE / TBS
        if l == 4:
            if t[3] == "BIG_TABLE":
                p = rst.Page()
                p.add(rst.SubSection("Listes des 10 plus grosses tables / applications "))
                doc.add(p)

            if mode == 1:
                print tabs,
                print "SubSections : %s " % t[3]

        ## Big_Table => Appli
        ## DB_CACHE => Donnees
        ## TBS => Donnees
        ## Banner => Donnees
        if l == 5:
            if t[4].startswith('REQUETE'):
                continue

            if t[3] == "TBS_SPACE" and t[4] == 'DATA':
                p = rst.Page()
                p.add(rst.SubSection("Etat des tablespaces : %s " % t[2] ))
                d = []
                d.append( ["TableSpace", "Alloue en Mo", "Utilise en Mo", "% Occupation"] )
                nom_tbs = []
                occ_tbs = []
                for l in data[cle][3:]:
                    d_tmp = l.split('!')
                    d.append(d_tmp)
                    nom_tbs.append( d_tmp[0].strip() )
                    occ_tbs.append( int(d_tmp[3]) )
                p.add(rst.Table(d))
                img_fic = "TBS_OCC.png"
                gr.tbs_graph( occ_tbs, nom_tbs, img_fic )
                p.add(rst.Image(img_fic))
                p.add( rst.Saut_Page() )
                doc.add(p)

            if t[3] == "BANNER" and t[4] == 'DATA':
                p = rst.Page()
                p.add(rst.SubSection("Banner Database  : %s " % t[2] ))
                for l in data[cle][3:]:
                    p.add(rst.Contenu( l ))
                doc.add(p)

            if t[3] == "BIG_TABLE":
                t[4] = "User / Application : %s " % t[4]

            if mode == 1:
                print tabs,
                print "S-SubSections : %s " % t[4]

        ## Big_Table => Appli => Donnees
        if l == 6:
            ## Les requetes c'est en cas de debug
            if t[5].startswith('REQUETE'):
                continue

            if t[3] == "BIG_TABLE" and t[5] == 'DATA':
                p = rst.Page()
                p.add(rst.Sub2Section("Application : %s " % t[4] ))
                d = None
                d = []
                d.append(["Nom de la Table ", "Nombre de lignes"] )
                for l in data[cle][3:13]:
                    d.append(l.split('!'))
                p.add(rst.Table(d))
                p.add( rst.Saut_Page() )
                doc.add(p)

            if mode == 1:
                print tabs,
                print "S-S-SubSections : %s " % t[5]
    else:
        if doc:
            print doc.render()
        
            


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
            gnr_rst(cles, data, mode=0)
        else:
            print "Fichier inexistant %s " % sys.argv[1]
