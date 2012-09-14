## ------------
## Trad_data
## ------------

# ----------------------------------------------------
# On part des donnees brutes en mode texte et on
# transforme cela en donnees utilisable
# par le gestionnaire de Rapport oracle
# ---------------------------------------------------

import os, sys
import pprint
from collections import namedtuple
from x_element import X_Element
        
## -------------------------------------------------------------------
## En Ligne     les heures 
## En colonne   les jours 
## Au croisement : 100 - % idle  ( 4 eme colonne )
## Ce qui devrait donner le pourcentage d'utilisation de la machine
## -------------------------------------------------------------------

import re
import pdb
import calendar
import time
import datetime
import locale


##
## Classe pour t_err (lecture log oracle)
##
class evenement(object):
    def __init__(self):
        self.vide = True
        self.date = ""
        self.data = []
        #print "\tCreate EVT"

    def contient_erreur(self):
        for l in self.data:
            if l.startswith('ORA-') or l.startswith('Errors'):
                return True
        return False

    def is_vide(self):
        return self.vide

    def __str__(self):
        return "[%s / %s]" % ( self.date, self.data )

## --------------------
## Quelques variables
## --------------------
locale.setlocale(locale.LC_ALL, 'fr_FR.UTF-8')

csv = {}
## ----------------------
## Lecture d'un fichier
## ----------------------
def lire_sar( ls ):
    day = time.localtime()[2]
    for l in ls:
        l = l.rstrip()
        m = re.match(".*([0-9][0-9])/([0-9][0-9])/([0-9][0-9]).*", l)
        if m:
            ## Si c'est un dimanche ou un samedi
            d = calendar.weekday( int(m.group(3)) ,int(m.group(1)) ,int(m.group(2)) )
            if d in [5,6]:
                ## On sort !
                break
            ## Debut on recupere la date M/D/Y => Y/M/D
            #d = "%s/%s/%s" % ( m.group(3),m.group(1),m.group(2) )
            t = datetime.datetime( int(m.group(3))+2000 ,int(m.group(1)) ,int(m.group(2)) )
            #d = "%s/%s" % ( m.group(1),m.group(2) )
            d = t.strftime("%d %m %Y")
            ## Cas particulier du calendrier
            if d.startswith('14 07') or d.startswith('25 12'):
                break
            ## On initialise la colonne
            csv[d] = {}
            #print "Jour = %s " % d
            continue
        if re.match("[0-9][0-9]", l):
            if re.match(".*usr.*", l):
                ## Ligne d'entete
                #print "+ %s " % l
                pass
            else:
                ## Ligne normale
                #print "- %s " % l
                # Dans certain cas je n'ai pas la colonne Proc %Physic
                try:
                    h,u,s,w,i,nb = re.split('\s+', l)
                except:
                    try:
                        h,u,s,w,i = re.split('\s+', l)
                    except:
                        h,u,s,w,i,phy,entc = re.split('\s+', l)
                h = h[:5]
                #print "h=%s u=%s s=%s w=%s i=%s" % ( h,u,s,w,i )
                csv[d].update({ h:100-int(i) })
        else:
            ## Autre ligne
            #print "> %s " % l
            pass

## -----------------------------------
## Recup des infos pour la description
## -----------------------------------
def t_sar(v):
    ## Creation de l'element de base pour sar
    d = X_Element( t='SAR' )
    fichier = ''
    for l in v:
        #print "====> %s " % l
        l = l.strip()
        if l.startswith('==>'):
            if fichier:
                lire_sar(f)
            ## Sinon on reprend
            fichier = l
            f = []
        else:
            f.append(l)
    else:
        lire_sar(f)

    ## -------------------------------
    ## Normalment ici j'ai mon csv{}
    ## -------------------------------
    # -----------------------------------------
    # Formattage des donnees
    # Une mesure tt les 10 minutes de 5h a 20h
    # -----------------------------------------
    for jour in csv.keys():
        for heure in range(5,20):
            for min in range(0,60,10):
                h = "%02d:%02d" % (heure, min)
                csv[jour].setdefault(h, 0)
    ## --------------------
    ## Generation de l'xml
    ## --------------------
    d.add(X_Element( t='titre' , v='Rapport Activite SAR'))
    data = X_Element( t='sar_data' )
    head = False
    moyenne ={}
    for k in csv.keys():
        jour = X_Element( t='Jour')
        jour.param("jour", k)
        jd = csv[k]
        kjd = jd.keys()
        kjd.sort()
        tmp_d = []
        tmp_h = []
        for vv in kjd:
            if int(vv[0:2]) >= 5 and int(vv[0:2]) <= 20 and int(vv[-1]) == 0:
                if not jd[vv]:
                    val = 0
                else:
                    val = jd[vv]
                tmp_d.append(val)
                tmp_h.append(vv)
                vv = vv.strip()
                if moyenne.has_key(vv):
                    moyenne[vv] += val
                else:
                    moyenne[vv] = val

        #h = X_Element( t='d', v="[%s,%s]" % (tmp_d, tmp_h) )
        if not head:
            head = True
            h = X_Element( t='heure', v="%s" % tmp_h )
            data.add(h)
        h = X_Element( t='d', v="%s" % tmp_d )
        jour.add(h)
        data.add(jour)
    ## Ajout de la moyenne
    nb_jour=len(csv.keys())
    mk = moyenne.keys()
    mk.sort()
    m = X_Element( t='moyenne', v="%s" % [moyenne[k]/nb_jour for k in mk ] )
    data.add(m)
    d.add(data)
    return d
        

## -----------------------------------
## Recup des infos pour la description
## -----------------------------------
def t_desc(v):
    d = X_Element( t='description' )
    for l in v:
        l=l.strip()
        if l.startswith("System Model"):
            d.add(X_Element(t='ref_ibm', v = l.split(":")[1]))
        elif l.startswith("Machine Serial Number"):
            d.add(X_Element(t='serial_num', v = l.split(":")[1]))
        elif l.startswith("Host Name"):
            d.add(X_Element(t='nom_hote', v = l.split(":")[1]))
        elif l.startswith("IP Address"):
            d.add(X_Element(t='ip_addr', v = l.split(":")[1]))
        elif l.startswith("Domain Name"):
            domain_name = l.split(":")[1]
            d.add(X_Element(t='domain_name', v = l.split(":")[1]))

    d.add(X_Element(t='base_ora', v = "X3 et PAIE"))
    d.add(X_Element(t='version_base', v = "9.2.0.4"))
    return d

## ------------------------------------------
## Recup des infos pour Instance / PGA
## ------------------------------------------
def t_pga(v):
    s = X_Element( t="MEM_PGA")
    row = X_Element( t="RowHead" )
    row.param("no", 0 )
    row.add(X_Element( t="ESTD_PC",  v='Pourcentage estime' ) )
    row.add(X_Element( t="PGA_TARGET", v='Cible PGA' ) )
    row.add(X_Element( t="PGA_TARGET_FACTOR", v='Facteur Cible PGA' ) )
    s.add(row)
    n = 0
    d={}
    for l in v:
        if l.startswith(''):
            n = 1
            continue
        if n == 1 and l.startswith('---'):
            n += 1
            continue
        if n >= 2:
            try:
                pga_t, pga_t_fe, adv, bp, eebrw, epch, eoc = l.split('!')
                pga_t = pga_t.strip()
                pga_t = int(int(pga_t)/1024)
                pga_t_fe = pga_t_fe.strip()
                pga_t_fe = pga_t_fe.replace(',','.')
                epch = epch.strip()
                row = X_Element( t="Row" )
                row.param("no", n-1)
                row.add(X_Element( t="ESTD_PC", v=epch ) )
                row.add(X_Element( t="PGA_TARGET_FACTOR", v=pga_t_fe ) )
                row.add(X_Element( t="PGA_TARGET", v=pga_t ) )
                s.add(row)
                n += 1
            except:
                pass
    return s

## ------------------------------------------
## Recup des infos pour Instance / DB_CACHE
## ------------------------------------------
def t_dbcache(v):
    s = X_Element( t="DB_CACHE")
    row = X_Element( t="RowHead" )
    row.param("no", 0 )
    row.add(X_Element( t="CACHE_SIZE",  v='Taille Cache TAMPON' ) )
    row.add(X_Element( t="SIZE_FACTOR", v='Facteur de Taille' ) )
    row.add(X_Element( t="ESTD_PB", v='Buffer(s) Physiques estimes' ) )
    row.add(X_Element( t="ESTD_PRF", v='Facteur Lecture(s) Physique(s) estimees' ) )
    row.add(X_Element( t="READS", v='Lecture' ) )
    s.add(row)
    n = 0
    d={}
    for l in v:
        if l.startswith(''):
            n = 1
            continue
        if n == 1 and l.startswith('---'):
            n += 1
            continue
        if n >= 2:
            try:
                cache_size, size_factor, estd_pb, estd_prf, reads = l.split('!')
                cache_size = cache_size.strip()
                #cache_size = int(int(cache_size)/1024)
                size_factor = size_factor.strip()
                size_factor = size_factor.replace(',','.')
                estd_pb = estd_pb.strip()
                estd_prf = estd_prf.strip()
                reads = reads.strip()
                row = X_Element( t="Row" )
                row.param("no", n-1)
                row.add(X_Element( t="CACHE_SIZE", v=cache_size ) )
                row.add(X_Element( t="SIZE_FACTOR", v=size_factor ) )
                row.add(X_Element( t="ESTD_PB", v=estd_pb ) )
                row.add(X_Element( t="ESTD_PRF", v=estd_prf ) )
                row.add(X_Element( t="READS", v=reads ) )
                s.add(row)
                n += 1
            except:
                pass
    return s

## ------------------------------------------
## Recup des infos pour Instance / Stockage
## ------------------------------------------
def t_big_table(v):
    s = X_Element( t="BIG_TABLE")
    row = X_Element( t="RowHead" )
    row.param("no", 0 )
    row.add(X_Element( t="nom_table",  v='Nom de la table' ) )
    row.add(X_Element( t="nb_lig", v='nb_lig' ) )
    s.add(row)
    n = 0
    d={}
    for l in v:
        if l.startswith(''):
            n = 1
            continue
        if n == 1 and l.startswith('---'):
            n += 1
            continue
        if n >= 2:
            name, nb = l.split('!')
            name = name.strip()
            try:
                nb = int(nb.strip())
            except:
                nb = 0
            d[name] = nb

    ## J'ai constitue moin dico
    ## Je le trie (merci la doc python)
    items = [(va, k) for k, va in d.items()]
    items.sort()
    items.reverse()
    items = [(k, va) for va, k in items]
    for k in items[0:20]:
        row = X_Element( t="Row" )
        row.param("no", n+1 )
        row.add(X_Element( t="nom_table",  v=k[0] ) )
        row.add(X_Element( t="nb_lig", v=k[1] ) )
        s.add(row)
    return s

## ----------------------------------
## Recup des infos pour Erreur Oracle
## ----------------------------------

def t_err_ora(ora_log):
    s = X_Element( t="Erreur Oracle")
    row = X_Element( t="RowHead" )
    row.add(X_Element( t="HDATE", v='Date / Heure' ) )
    row.add(X_Element( t="DESC", v='Description / Requete' ) )
    s.add(row)

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

    evt = evenement()
    n = 0

    for ligne in ora_log:
        ligne = ligne.strip()
        #print "-> Ligne %s " % ligne
        result = p.match(ligne)
        if result:
            #print "\t\t>> MATCH %s " % ligne
            if not evt.is_vide():
                #print "\t\tNon Vide on traite"
                do_the_work(n, s, evt)
                n += 1
            #print "\t\tVide On renseigne la date"
            evt = evenement()
            evt.date = ligne
            evt.vide = False
        else:
            #print "\t\tNOT MATCH %s " % ligne
            #print "\t\tAjout dans %s" % evt
            evt.data.append(ligne)
            evt.vide = False
    else:
        do_the_work(n, s, evt)
    s.param("nb_ligne", n-2 )
    return s

def do_the_work( n, s, evt ):
    if evt.date:
        if evt.contient_erreur():
            #print "\tDO THE WORK ON %s " % evt
            row = X_Element( t="Row" )
            row.param("no", n-1)
            row.add(X_Element( t="HDATE", v=evt.date ) )
            #pdb.set_trace()
            desc = modif_car(evt.data)
            row.add(X_Element( t="DESC", v=desc))
            s.add(row)
    #else:
        #print "\tPas de date => %s " % evt

#def t_err_ora(v):
#    s = X_Element( t="Erreur Oracle")
#    row = X_Element( t="RowHead" )
#    row.add(X_Element( t="HDATE", v='Date / Heure' ) )
#    row.add(X_Element( t="DESC", v='Description / Requete' ) )
#    s.add(row)
#    p = re.compile(r"""
#        ^                           # Au debut
#        [A-Z][a-z][a-z]             # Jour
#        \s*
#        [A-Z][a-z][a-z]             # Mois
#        \s*
#        [0-9]{1,2}                  # Jour
#        \s*
#        [0-9]{2}:[0-9]{2}:[0-9]{2}  # Heure
#        \s*
#        [0-9]{4}                    # Annee
#        \s*
#        $                           # A la fin
#        """, re.VERBOSE)
#
#    h = ""
#    t = []
#    n = 0
#    for l in v:
#        r = p.match(l)
#        print "%s / %s " % (r, l)
#        if r:
#            if h == l:
#                t.append(l)
#            else:
#                if len(t):
#                    if t[0].startswith('ORA-') or t[0].startswith('Error'):
#                        print "*** "
#                        row = X_Element( t="Row" )
#                        row.param("no", n-1)
#                        row.add(X_Element( t="HDATE", v=h ) )
#                        #pdb.set_trace()
#                        desc = modif_car(t)
#                        row.add(X_Element( t="DESC", v=desc))
#                        s.add(row)
#                        n += 1
#                print "h=%s t=%s" % (h, t)
#                h = l
#                t = []
#        else:
#            t.append(l)
#
#    s.param("nb_ligne", n-2 )
#    return s

def modif_car(data):
    d = [ x.replace('<', 'inf') for x in data ]
    d = [ x.replace('>', 'sup') for x in d ]
    return d

## ------------------------------------------
## Recup des infos pour Instance / Stockage
## ------------------------------------------
def t_stockage(v):
    s = X_Element( t="Stockage")
    row = X_Element( t="RowHead" )
    row.param("no", 0 )
    row.add(X_Element( t="TBS", v='Tablespace' ) )
    row.add(X_Element( t="PCUSED", v='% Utilise' ) )
    row.add(X_Element( t="DISPO", v='Disponible' ) )
    row.add(X_Element( t="TAILLE", v='Taille' ) )
    s.add(row)
    n = 0
    for l in v:
        if l.startswith('Tablespace'):
            n += 1
        if n == 1:
            n = 2
            continue
        if n >= 2:
            if l.startswith('-'):
                continue
            if l.startswith('\t'):
                break
            tbs, pc, dispo, taille = l.split('!')
            row = X_Element( t="Row" )
            row.param("no", n-1)
            row.add(X_Element( t="TBS", v=tbs ) )
            try:
                pc = 100-int(pc)
            except:
                pc = 0
            row.add(X_Element( t="PCUSED", v=pc ) )
            row.add(X_Element( t="DISPO", v=dispo ) )
            row.add(X_Element( t="TAILLE", v=taille ) )
            s.add(row)
            n += 1
    s.param("nb_ligne", n-2 )
    return s

def convert(n):
    try:
        r = int(n)
    except:
        r = 0
    return r


## ------------------------------------------
## Recup des infos pour L'entete
## ------------------------------------------
def t_sga(v):
    m = X_Element( t="Memoire" )
    d = {
       'FIXED_SIZE'                 :0,
       'VARIABLE_SIZE'              :0,
       'DATABASE_BUFFERS'           :0,
       'REDO_BUFFERS'               :0,
       'LARGE_POOL'                 :0,
       'JAVA_POOL'                  :0,
       'SHARED_POOL'                :0,
    }
    for l in v:
        try:
            name, value = l.split('!')
        except:
            continue
        value = convert(value)
        value = value/1024
        value = int(((value+0.5)*100)/100)
        if l.startswith('Fixed Size'):
            d["FIXED_SIZE"]=value
        if l.startswith('Variable Size'):
            d["VARIABLE_SIZE"]=value
        if l.startswith('Database Buffers'):
            d["DATABASE_BUFFERS"]=value
        if l.startswith('Redo Buffers'):
            d["REDO_BUFFERS"]=value
        if l.startswith('java pool'):
            d["JAVA_POOL"]=value
        if l.startswith('large pool'):
            d["LARGE_POOL"]=value
        if l.startswith('shared pool'):
            d["SHARED_POOL"]=value

    for k in d.keys():
        t = X_Element(t=k, v=d[k])
        t.numeric = True
        m.add(t)
    return(m)

## ------------------------------------------
## Recup des infos pour L'entete
## ------------------------------------------
def t_ent(v):
    e = X_Element( t='entete' )
    for l in v:
        if l.startswith('Genere le'):
            h = l[11:20]
            d = l[20:29]
    e.add( X_Element( t='titre', v= "Rapport ORACLE \nMensuel" ))
    e.add( X_Element( t='auteur', v= "AUTEUR" ))
    e.add( X_Element( t='version', v= "0.0 Alpha" ))
    e.add( X_Element( t='diffusion', v= "INTERNE" ))
    e.add( X_Element( t='genere_le', v= "le %s a %s" % (d, h) ))
    return e

## ------------------------------------
## Recup des infos pour SYSTEME DISK
## ------------------------------------
def t_sys_disk(v):

    s = X_Element(t="SYS_DISK")
    r = X_Element(t="RowHead")
    r.add(X_Element( t="fs", v="Systeme de Fichier" ))
    r.add(X_Element( t="vu", v="Volume Utilise" ))
    r.add(X_Element( t="vl", v="Espace libre" ))
    r.param("no", 0)
    s.add(r)
    n = 1
    for l in v:
        if l.startswith('/'):
            fs, vtot, vlibre, vutil, pcu, pcl, nom= l.split()
            ## Faut le faire apres
            #if nom in ( '/data1', '/data2', '/oracle' ):
            r = X_Element(t="Row")
            r.param("no", n)
            r.add(X_Element( t="fs", v="%s %s" % (fs, nom)  ))
            r.add(X_Element( t="vu", v="%s" % vtot ))
            r.add(X_Element( t="vl", v="%s" % vlibre))
            s.add(r)
            n += 1
    s.param("nb_ligne", n-1 )
    return s

## ---------------------
## Traduire les donnees
## ---------------------
def traduire(dat):
    ### ON commence
    r = X_Element( t='root' )

    instance = {}

    ## C'est parti
    for k,v in dat.items():
        #print "Cle = %s " % k
        if k == "DESC":
            r.add(t_desc(v))

        if k == "SAR":
            r.add(t_sar(v))

        if k == "ENT":
            r.add(t_ent(v))
            
        if k == "SYS_DISK":
           r.add(t_sys_disk(v))

        if k.endswith("DB_CACHE"):
            i = k.split('.')[0]
            if not instance.has_key(i):
                instance[i] = X_Element(t='Instance', v=i)
                instance[i].param("name", i)
            instance[i].add(t_dbcache(v))

        if k.endswith("PGA"):
            i = k.split('.')[0]
            if not instance.has_key(i):
                instance[i] = X_Element(t='Instance', v=i)
                instance[i].param("name", i)
            instance[i].add(t_pga(v))

        if k.endswith("BIG_TABLE"):
            i = k.split('.')[0]
            if not instance.has_key(i):
                instance[i] = X_Element(t='Instance', v=i)
                instance[i].param("name", i)
            instance[i].add(t_big_table(v))

        if k.endswith('SGA'):
            i = k.split('.')[0]
            if not instance.has_key(i):
                instance[i] = X_Element(t='Instance', v=i)
                instance[i].param("name", i)
            instance[i].add(t_sga(v))
            
        if k.endswith('Stockage'):
            i = k.split('.')[0]
            if not instance.has_key(i):
                instance[i] = X_Element(t='Instance', v=i)
                instance[i].param("name", i)
            instance[i].add(t_stockage(v))

        if k.endswith('ERR_ORA'):
            i = k.split('.')[0]
            if not instance.has_key(i):
                instance[i] = X_Element(t='Instance', v=i)
                instance[i].param("name", i)
            instance[i].add(t_err_ora(v))

    for i in instance.keys():
        r.add(instance[i])

    return r

## Calcul de la cle
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
    cle = ""
    for l in open(fichier, 'r').readlines():
        if l.startswith(ENT_CHAPITRE):
            l = l.strip()
            if l.endswith(DEB_CHAP):
                c = trad_cle(l)
                if not cle:
                    cle = c
                    chap[c] = []
                else:
                    print "ERREUR CHAPITRE "
                    sys.exit(1)
            elif l.endswith(FIN_CHAP):
                c= trad_cle(l)
                if c == cle:
                    cle = ""
                else:
                    print "ERREUR CHAPITRE "
                    sys.exit(1)
            else:
                pass
        else:
            chap[cle].append(l.rstrip())
    return chap

## ------------------------------
## impression d 'un fichier csv
## Pour integration dans Tableur
## Pour debug au cas ou
## -----------------------------
def prt_csv():
    #pdb.set_trace()
    #print "=" * 50
    #print csv
    
    ## Generation d'un point CSV 
    col = csv.keys()
    col.sort()
    lig = csv[col[0]].keys()
    lig.sort()
    ## Les entetes
    #SEP="\t"
    SEP=","
    print '"HEURE"',SEP,
    for c in col:
        print '"%s"' % c,SEP,
    print
    t = csv[c].keys()
    t.sort()
    #COL_VIDE = "<>"
    COL_VIDE = "0"
    for l in t:
        ## Je ne prend que de 5h00 a 20h00
        if int(l[0:2]) >= 5 and int(l[0:2]) <= 20:
            print "%s" % l,SEP,
            for c in col:
                li = csv[c]
                x = li.get(l, COL_VIDE ),
                print "%s" % x,SEP,
                if x == (COL_VIDE,):
                    pass
                    #print "====> c=%s csv[c]=%s" % (c, li)
            print
   
if __name__ == '__main__':
    if len(sys.argv) > 1:
        if os.path.exists(sys.argv[1]):
            data = lire(sys.argv[1])
            r = traduire(data)
            print r.pr()
        else:
            print "Fichier inexistant %s " % sys.argv[1]
    else:
        fichier="nasa_09_juin_2011.txt"
        data = lire(fichier)
        r = traduire(data)
        print r.pr()
