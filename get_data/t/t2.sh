
APPLI="X3/DEMOFRA/TOTO/TUTU"

echo "$APPLI" | tr "/" "\n" |
while read APPLI
do
	echo $APPLI
done
