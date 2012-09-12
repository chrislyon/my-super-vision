## -------------------------------
## Makefile Generique
## Attention GMAKE obligatoire
## -------------------------------
## Makefile de base pour des projets 
## python
## -------------------------------
## make all     => Affichage du message concernant gmake
## make run     => lance le programme principal
## make test    => lance avec -v pour doctest
## make lint    => lance pylint sur tout les *.py
## make debug   => Lance avec mode debug
## make status  => lance svn status
## make clean   => fait le menage 
## make id      => met a jour avec svn keyword:id
## make install => lance une installation

# $Id: $

LIB=
DATA=
BIN=rtext
## Rep
BASE_DIR=$(shell pwd)
#BASE_DIR=/chemin/absolu
DIST_DIR=$(BASE_DIR)/distrib
LOG_DIR=log
HOST=$(shell hostname)
SRC=$(LIB) $(DATA) $(BASE_DIR)
MSG_TXT="message.txt"

RCLINT_FILE=pylintrc

## Variable pour entete
PYTHON=$(shell which python)
PROJET="NOM_DU_PROJET"
VERSION="Alpha 0.0"
DATE_CR=$(shell date "+%x %X")
ANNEE=$(shell date "+%Y")
AUTEUR=chris

OPT=-v -f conf/autre.conf
OPT=""
MSG_TXT="Message.txt"
MSG_TXT=""

all:
	echo "MAKE => $(MAKE)"
	echo "ATTENTION GMAKE Necessaire ..."

.PHONY: clean
clean:
	rm -f *.pyc
	rm -f */*.pyc
	rm -fr $(DIST_DIR)
	rm -fr $(DATA_DIR)
	rm -f *.log
	rm -f $(LOG_DIR)/*.log

.PHONY: clean_inst
clean_inst:
	rm -fr $(DIST_DIR)

.PHONY: do_install
do_install: 
	[ -d $(DIST_DIR) ] || mkdir $(DIST_DIR)
	cp -r $(LIB) $(DIST_DIR)
	cp -r $(DATA) $(DIST_DIR)
	cp $(BIN).py $(DIST_DIR)
	## Copie shellscript avec modif du base_dir
	cat $(SHELL_SCRIPT) | \
		sed -e "s!%%_BASE_DIR_%%!$(DIST_DIR)!" > $(DIST_DIR)/$(BIN)
	chmod +x $(DIST_DIR)/$(BIN)
	cp $(DEF_CONF_FILE) $(DIST_DIR)/$(DEF_CONF)
	[ "$(HOST)" == "SRADEV" ] && \
		cp $(TEST_CONF_FILE) $(DIST_DIR)/data.perfanl

.PHONY: install
install: do_install
	echo "Rock and Roll !!"

.PHONY: inst_test
inst_test: clean_inst install
	echo "TEST => Rock and Roll !!"

.PHONY: status
status: clean
	svn status

.PHONY: id
id: clean
	for i in `find . -name "*.py"` ; do \
		echo "je traite $$i" ;\
		[ ! -d $$i ] && svn ps svn:keywords Id $${i} ; \
	done

.PHONY: run
run:
	python $(BIN).py $(OPT) $(MSG_TXT)

.PHONY: test
test:
	python $(BIN).py -v $(OPT) $(MSG_TXT)

.PHONY: lint_all
lint_all:
	for i in `find . -name "*.py"` ; do \
		echo "je traite $$i" ;\
		[ ! -d $$i ] && pylint --rcfile $(RCLINT_FILE) $${i} ;\
	done

.PHONY: lint
lint:
	pylint --rcfile $(RCLINT_FILE) *.py

.PHONY: debug
debug:
	python $(BIN).py

.PHONY: entete
entete:
	@echo "#! " $(PYTHON)
	@echo "# -*- coding: UTF8 -*-"
	@echo "##----------------------------------------------------"
	@echo "## Projet        : " $(PROJET)
	@echo "## Version       : " $(VERSION)
	@echo "## Auteur        : " $(AUTEUR)
	@echo "## Date Creation : " $(DATE_CR)
	@echo "## Objet         : "
	@echo "## MAJ           : "
	@echo "## Bug Report    : "
	@echo "## Todo List     : "
	@echo "##----------------------------------------------------"
	@echo '## $$Id :$$'
	@echo "##----------------------------------------------------"
	@echo "## (c) " $(AUTEUR) $(ANNEE)
	@echo "##----------------------------------------------------"
	@echo '"""'
	@echo "Doc String du Module (evite mauvaise note a lint)"
	@echo '"""'
	@echo "# import "
	@echo "import sys"
	@echo "# constants"
	@echo "# exception class"
	@echo "# interface function"
	@echo "# classes"
	@echo "# internal function and classes"
	@echo "def main(arg):"
	@echo '    """Fonction main qui dit bonjour """'
	@echo '    retour = "BONJOUR %s" % arg'
	@echo "    return retour"
	@echo ""
	@echo "if __name__ == '__main__':"
	@echo "    R_ST = main('LE MONDE')"
	@echo "    sys.exit(R_ST)"
