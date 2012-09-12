:
## ---------------------------------------
## Recup des infos pour le rapport Oracle
## ---------------------------------------

DJ=`date "+%X %x"`
SID="X3"

## --------
## Log 
## --------
log()
{
	m="<VIDE>"
	[ "$1" ] && m=$1
	printf "#>>>:%s:#\n" $m
}

## --------
## DO SQL
## --------
do_sql()
{
	user=$1
	shift
	SID=$1
	shift
	db_user=$1
	shift
	req="$*"
	TEMP_FILE=/tmp/do_sql$$.sql
	rm -f $TEMP_FILE
	( echo SET NEWPAGE 0
	echo SET SPACE 0
	echo SET LINESIZE 2000
	echo SET PAGESIZE 5000
	echo SET ECHO OFF
	echo SET FEEDBACK OFF
	echo SET VERIFY OFF
	echo SET MARKUP HTML OFF SPOOL OFF
	echo SET HEADING ON
	echo set colsep "!" ) > $TEMP_FILE
	echo "$req" >> $TEMP_FILE
	printf "exit\n/\n\nquit\nquit\n" >> $TEMP_FILE
	#echo "user=$user sid=$SID req=[$req]"
	#cat $TEMP_FILE
	su - ${user} -c ". /oracle/product/9.2.0/.profile ; export ORACLE_SID=$SID;sqlplus -S $db_user @$TEMP_FILE"
	rm -f $TEMP_FILE
}

## -----------------------
## Generation d'un entete
## -----------------------
entete()
{
	log "ENT-DEB"
	echo "Genere le " $DJ
	log "ENT-FIN"
}

## -------------
## Description
## -------------
desc()
{
	log "DESC-DEB"
	export LANG=C
	prtconf
	log "DESC-FIN"
}

## ----------
## SYSTEME
## ----------
## Disques 
sys_disk()
{
	log "SYS_DISK-DEB"
	df -g
	log "SYS_DISK-FIN"
}
## Erreur SYSTEME
sys_err()
{
	log "SYS_ERR-DEB"
	errpt -a
	log "SYS_ERR-FIN"
}

## ----
## SAR
## ----
SAR()
{
	log "SAR-DEB"
	D=/var/adm/sa
	for f in $D/sa[0-9][0-9]*
	do
		echo "==> $f"
		sar -u -f $f
	done
	log "SAR-FIN"
}

## ------------------------------------
## Recup des erreurs oracle
## A voir gestion des fichiers .trc
## ------------------------------------
ora_err()
{
	fichier=$1
	ts=`date "+%Y_%m_%d_%X"`
	if [ -f $fichier ]
	then
		## sav/copie du fichier
		cp $fichier $fichier.$ts
		## Raz fichier 
		#>$fichier
		## recup du fichier copie
		cat $fichier.$ts
	fi

}

#entete
entete
#Description
## nom_hote
## adr_ip
## ref_ibm
## base_ora
desc
#Resume
# A Saisir

## ===============================================
## Pour chaque instance (SID)
## SID.Memoire
# CGE
DIR=`pwd`
user=ora920
SID=X3
db_user=system/manager
log_ora=/ado/cge/X3V5/database/dumpdir/alert_CGE.log
## ==============================================
log "X3.PARAM-DEB"
echo "Repertoire : $DIR"
echo "user       : $user"
echo "SID        : $SID"
echo "db_user    : $db_user"
log "X3.PARAM-FIN"
## ==============================================
log "X3.SGA-DEB"
do_sql $user $SID $db_user "@$DIR/sga.sql"
log "X3.SGA-FIN"
## SID.Pool
log "X3.PGA-DEB"
do_sql $user $SID $db_user "@$DIR/pga.sql"
log "X3.PGA-FIN"
## SID.DB_cache
log "X3.DB_CACHE-DEB"
do_sql $user $SID $db_user "@$DIR/db_cache.sql"
log "X3.DB_CACHE-FIN"
## SID.MEM_PGA
##
##
##
## SID.TOP_SQL
log "X3.TOP_SQL-DEB"
do_sql $user $SID $db_user "@$DIR/top_sql.sql"
log "X3.TOP_SQL-FIN"
## SID.Stockage
log "X3.Stockage-DEB"
do_sql $user $SID $db_user "@$DIR/tbs.sql"
log "X3.Stockage-FIN"
## SID.BIG_TABLE
log "X3.BIG_TABLE-DEB"
do_sql $user $SID $db_user "@$DIR/big_table.sql"
log "X3.BIG_TABLE-FIN"
## SID.ERR_ORA
log "X3.ERR_ORA-DEB"
#ora_err $log_ora
log "X3.ERR_ORA-FIN"

## SAR
SAR

## Systeme
## SYS.DISK
sys_disk
## Et tout est deja en Giga
## SYS.ERR
sys_err
