
BIN=rtext

PYTHON=$(shell which python)

OUTPUT_FILE=toto

all:
	echo "MAKE => $(MAKE)"
	echo "ATTENTION GMAKE Necessaire ..."

run:
	$(PYTHON) $(BIN)

odt:
	rm -f $(OUTPUT_FILE).odt
	$(PYTHON) $(BIN).py | rst2odt --stylesheet=my_styles.odt > $(OUTPUT_FILE).odt
	soffice $(OUTPUT_FILE).odt

pdf:
	rm -f $(OUTPUT_FILE).pdf
	$(PYTHON) $(BIN).py | rst2pdf > $(OUTPUT_FILE).pdf
	evince $(OUTPUT_FILE).pdf

html:
	rm -f $(OUTPUT_FILE).pdf
	$(PYTHON) $(BIN).py | rst2html > $(OUTPUT_FILE).html
	firefox $(OUTPUT_FILE).html

clean:
	rm -f $(OUTPUT_FILE).*
