
cat <<-EOF | tr "[a-z]" "[A-Z"] \
	 | sed -s "s/A/X/g"
salut la compagnie
EOF

A="
salut la compagnie
ligne 2 \"guillemet\"
ligne 3		tab
"

echo "=====> $A"


do_sql()
{
	sql=$(cat)
	echo "=>$sql<="
}

do_sql << EOF
	TEST AVEC PLEIN DE CHOSES
	"GUILLEMET"
	\" autres \"
	sqlplus system/manager
EOF
