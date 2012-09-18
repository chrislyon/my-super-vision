#!  /usr/bin/python
# -*- coding: UTF8 -*-
##----------------------------------------------------
## Projet        :  Restructured Text Generator
## Version       :  Alpha 0.0
## Auteur        :  chris
## Date Creation :  11/09/2012 13:19:10
## Objet         : 
## MAJ           : 
## Bug Report    : 
## Todo List     : 
##----------------------------------------------------
## $Id :$
##----------------------------------------------------
## (c)  chris 2012
##----------------------------------------------------
"""
    Generation de fichier en restructured text
"""

import sys
import pdb

class Fichier(object):
    """
        Un fichier regroupe des pages
    """
    def __init__(self):
        self.name = ""
        self.pages = []

    def add(self, p):
        self.pages.append(p)

    def render(self):
        for p in self.pages:
            print p.render()

class Page(object):
    """
        Une page regroupe des contenus
    """
    def __init__(self):
        self.contenu = []

    def add(self, p):
        self.contenu.append(p)

    def render(self):
        r = ''
        for c in self.contenu:
            r += c.render()
        return r

class Contenu(object):
    """
        Un contenu represente du texte
        avec un methode render => pour generer du RestructuredText
    """
    def __init__(self, texte=None):
        self.val = texte

    def render(self):
        return self.val+"\n\n"

class Entete(Contenu):
    """
        Entete permet de mettre la directive pour numeroter 
        les sections et inserer la table des matières
    """
    def __init__(self, texte = "Table des matières" ):
        self.val = texte

    def render(self):
        r = ".. sectnum::\n\n"
        r += ".. contents:: "+self.val
        r += "\n\n"
        return r

class Titre(Contenu):
    """
        Le titre de la page
    """

    def render(self):
        l = len(self.val)
        r = ""
        r += "=" * l + "\n"
        r += "%s\n" % self.val
        r += "=" * l
        r += "\n\n"
        return r

class Section(Contenu):
    """
        Une section = Titre 1
    """

    def render(self):
        l = len(self.val)
        r = ""
        r += "%s\n" % self.val
        r += "~" * l 
        r += "\n\n"
        return r

class SubSection(Contenu):
    """
        Une Sous section = Titre 2
    """

    def render(self):
        l = len(self.val)
        r = ""
        r += "%s\n" % self.val
        r += "-" * l
        r += "\n\n"
        return r

class Code(Contenu):
    """
        Du code non modifiable 
    """
    def render(self):
        r = ""
        r += "::\n"
        r += "\n"
        r += "%s" % self.val
        r += "\n"
        return r

class Table(Contenu):
    """
        Contenu = un tableau
        1 ere ligne = Entete de colonne
    """
    def to_csv(self,data):
        return '"%s"' % data

    def render(self):
        r = ""
        r += ".. csv-table:: "
        r += "\n"
        h = self.val.pop(0) # Premiere ligne
        r += "\t:header: "
        r += ",".join(map(self.to_csv, h))
        r += "\n"
        r += "\n"
            
        for l in self.val:
            r += "\t"
            r += ",".join(map(self.to_csv,l))
            r += "\n"

        r += "\n"
        r += "\n"
        return r
            
        
# internal function and classes
def test():

    f = Fichier()

    p = Page()
    f.add(p)


    tt = """
        Ceci est un texte 
        """
    tt1 = """        Lorem ipsum dolor sit amet, consectetur adipiscing elit. Etiam a neque vel neque iaculis pharetra molestie sed quam. Fusce facilisis metus a augue laoreet pharetra. In pellentesque luctus tellus, a rutrum quam iaculis luctus. Duis commodo sodales pellentesque. Nulla facilisi. Suspendisse erat nisi, sagittis nec varius vel, aliquam vitae diam. Maecenas sit amet justo et justo convallis lobortis quis sed nibh. Donec at arcu eget lacus fermentum rutrum eu eget eros. Proin eget felis nec sapien interdum accumsan vel in velit. Donec at erat eu odio dictum consequat ac convallis velit. Proin ullamcorper egestas tristique. Praesent ante neque, mollis non posuere id, facilisis sed leo. Nam eget velit sed nibh vehicula consequat ut ut magna. Mauris aliquet pulvinar lacus, eget fringilla enim venenatis vitae. Suspendisse congue sagittis arcu, eu lacinia magna hendrerit a.
"""

    tt2 = """
         Vivamus et tellus in felis convallis congue. Quisque dignissim vulputate sapien eget pharetra. Etiam condimentum condimentum mauris, a imperdiet leo consectetur vel. Quisque suscipit tempor sapien, eget venenatis mauris rutrum et. In elementum bibendum mauris at mollis. Cras placerat lacinia eros vitae vulputate. Vestibulum fringilla tempus justo, venenatis tempus odio egestas in. Praesent suscipit, nisl id venenatis hendrerit, purus tellus tincidunt nisl, et consectetur orci purus id mi.
    """

    tt3 = """
         Morbi convallis nunc a sapien venenatis at dictum felis malesuada. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Vivamus tempus, lacus sit amet vehicula scelerisque, sem lacus tristique ligula, hendrerit posuere sapien lectus ornare ante. Fusce id arcu hendrerit nisl placerat viverra in vitae sapien. Aenean congue sollicitudin dignissim. Proin fringilla, purus eu pellentesque scelerisque, erat tellus facilisis augue, vitae sodales libero arcu at ligula. In nec urna orci. Donec quam magna, tristique nec ornare quis, semper vitae ligula. Integer quis odio mauris. Sed ut tortor nec augue ornare volutpat. Nullam non nisl non risus iaculis sodales sed quis mauris. Nullam dignissim feugiat malesuada. 
    """

    p.add( Titre("TITRE DE LA PAGE") )
    p.add( Entete())
    p.add(Section("Section 1"))
    p.add( Contenu(tt) )
    p.add(Section("Section 2"))
    p.add(SubSection("SousSection"))
    p.add( Contenu( "TEXTE BIDON ") )
    p.add(SubSection("SousSection"))
    p.add( Contenu( "TEXTE BIDON ") )
    p.add(SubSection("SousSection"))
    p.add( Contenu( "TEXTE BIDON ") )
    p.add(SubSection("SousSection"))
    p.add( Contenu(tt1) )
    p.add(Section("Section 3"))
    p.add( Contenu(tt2) )
    p.add(Section("Section 4"))
    p.add( Contenu(tt3) )

    C1 = """
        24 class Fichier(object):
        28     def __init__(self):
        29         self.name = ""
        30         self.pages = []
        31 
        32     def add(self, p):
        33         self.pages.append(p)
        34 
        35     def render(self):
        36         for p in self.pages:
        37             print p.render()

        """
    p.add(Section("Section 5"))
    p.add( Code(C1) )

    ## Exemple de table
    p.add(Section("Section 4"))
    ta = [
        ( "Description ", "Qte", "Prix Unitaire", "Total" ),
        ("Produit 1", 5, 200, 5*200 ),
        ("Produit 2", 4, 230, 4*230 ),
        ("Produit 3", 8, 250, 8*250 ),
        ("Produit 4", 8, 220, 8*220 ),
    ]
    p.add( Table(ta) )


    f.render()


if __name__ == '__main__':
    test()
