#! /bin/bash

## =================
## GET DATA
## =================
## Chris (2012)

DJ=$(date "+%d-%m-%y %H:%M:%S")

## ---------------
## Routine de log
## ---------------
log()
{
	m="<VIDE>"
	[ "$1" ] && m="$1"
	printf "#>>>:%s:#\n" "$m"
}

## --------------------
## recupere les infos
## --------------------
get_conf()
{
	## Database
	## SID ou Nom Base (pour info)
	## User 
	## Login/passe BDD
	## HOST/SID => si accès distant sinon rien
	## SQLPLUS
	SQLPLUS=$(which sqlplus64)
	APPLI="X3/DEMOFRA/GRPSRAHOTX/GRPSRAHOTL/TOTO/FRBV5"
	DATABASE="SRADEV2_X3V5::system/manager:sradev2/X3V5:$SQLPLUS:$APPLI"
}

## -----------------------
## Generation d'un entete
## -----------------------
entete()
{
	log "ENT-DEB"
	echo "GET_DATA V0.0Alpha"
	echo "Genere le " $DJ
	log "ENT-FIN"
}


##
## Description du serveur
##
serveur_desc()
{
	log "SERVEUR_DESC-DEB"
	echo "SERVER_NAME:" $(hostname -A)
	echo "SERVER IP:" $(hostname -i)
	echo "SERVER UNAME:" $(uname -a)
	echo "SERVER RELEASE:" $(cat /etc/system-release)
	log "SERVEUR_DESC-FIN"
}

## -----------
## Serveur DF 
## Ressources disques
## -----------
serveur_df()
{
	log "SERVEUR_DF-DEB"
	echo "SERVER_NAME:" $(hostname -A)
	df -kP
	log "SERVEUR_DF-FIN"
}

## -----------------------------
## Execution d'un requete SQL
## -----------------------------
do_sql()
{
	
	ENT="
	SET NEWPAGE 1
	SET SPACE 0
	SET LINESIZE 2000
	SET PAGESIZE 5000
	SET ECHO OFF
	SET FEEDBACK OFF
	SET VERIFY OFF
	SET MARKUP HTML OFF SPOOL OFF
	SET HEADING ON
	SET TAB OFF
	set colsep \"!\"
	"
	req=$(cat)
	log "REQUETE-DEB"
	echo "$ENT $req"
	log "REQUETE-FIN"
	log "REQUETE_EXE-DEB"
	echo "Exec => ${ORA_USER} ${SQLPLUS} ${LOGIN_BDD}@${TNS}"
	log "REQUETE_EXE-FIN"
	## execution de la requete
	log "DATA-DEB"
	echo "${ENT} ${req}" | su - ${ORA_USER} -c "${SQLPLUS} -S ${LOGIN_BDD}@${TNS}"
	log "DATA-FIN"
	## saut de 1 ligne
	echo
		
}

## ---------------------------
## Liste des applications
## ---------------------------
liste_appli_SQL()
{
	log "LISTE_APPLI_SQL-DEB"
	do_sql << EOF
	select distinct grantee
	from DBA_ROLE_PRIVS
	where granted_role like '%ADX%'
	and grantee != 'SYS'
	and grantee != 'SYSTEM'
	and grantee not like '%REPORT'
	order by grantee;
EOF
	log "LISTE_APPLI_SQL-FIN"
}

## ---------------------
## TABLESPACE USAGE
## ---------------------
TBS_usage_SQL()
{
	log "TBS_SPACE_SQL-DEB"
	do_sql << EOF
	SELECT
		df.tablespace_name TBS,
		round(df.bytes/1024/1024) Alloue_Mo,
		round(free.free_Mo) Libre_Mo,
		100-Round(free.free_Mo/(df.bytes/1024/1024)*100) Usage_pourcent
	FROM
		dba_data_files df,
		(SELECT file_id, SUM(bytes)/1024/1024 free_Mo
	FROM dba_free_space GROUP BY file_id) free
	WHERE
		df.file_id=free.file_id
	ORDER BY
		TABLESPACE_NAME;
EOF
	log "TBS_SPACE_SQL-FIN"
}

## ------------------
## DB BUFFER CACHE
## ------------------
DB_buffer_cache_SQL()
{
	log "DB_BUFFER_CACHE_SQL-DEB"
	do_sql << EOF
	SELECT
		size_for_estimate,
		size_factor,
		buffers_for_estimate,
		estd_physical_read_factor,
		estd_physical_reads
	FROM
		v\$db_cache_advice
	WHERE
		name = 'DEFAULT'
	AND
		block_size =
		(
			SELECT value FROM v\$parameter
			WHERE name = 'db_block_size'
		)
	AND
		advice_status = 'ON';
EOF
	log "DB_BUFFER_CACHE_SQL-FIN"
}

## ----------------------
## TEST SQL (MODELE)
## ----------------------
## Exemple de requete sql 
## NE PAS OUBLIER LE ; a la fin
test_SQL()
{
	log "TEST_SQL-DEB"
	do_sql << EOF
		select * from all_users;
EOF
	log "TEST_SQL-FIN"
}

## ----------------------
## BANNER DATABASE
## ----------------------
banner_SQL()
{
	log "BANNER-DEB"
	do_sql << EOF
		select banner from v\$version;
EOF
	log "BANNER-FIN"
}

## ----------------------
## Taille Table / Appli
## ----------------------
big_table_SQL()
{
	log "BIG_TABLE-DEB"
	echo "$APPLI" | tr "/" "\n" | \
	while read apl
	do
	log "${apl}-DEB"
	do_sql << EOF
	col table_name format a30
	col num_rows format 999999999
	select table_name, num_rows
	from dba_tables
	where owner='${apl}'
	order by 2 desc;
EOF
	log "${apl}-FIN"
	done
	log "BIG_TABLE-FIN"
}

## ----------------------
## Une base de données
## ----------------------
get_DB()
{
	DATA=$1
	DB=$(echo $DATA | cut -d: -f1)
	ORA_USER=$(echo $DATA | cut -d: -f2)
	LOGIN_BDD=$(echo $DATA | cut -d: -f3)
	TNS=$(echo $DATA | cut -d: -f4)
	SQLPLUS=$(echo $DATA | cut -d: -f5)
	APPLI=$(echo $DATA | cut -d: -f6)

	#test_SQL		# Test du SQL
	#liste_appli_SQL	# Liste des applis X3
	banner_SQL		# Bannner Version
	big_table_SQL	# Tables dans l'ordre du nb de lignes
	TBS_usage_SQL
	DB_buffer_cache_SQL
}

## --------------------------
## traitement des serveurs
## --------------------------
serveurs()
{
	log "SERVEURS-DEB"
	serveur_desc
	serveur_df
	log "SERVEURS-FIN"
}

## =================================
## Traitement des bases de données
## =================================
databases()
{
	log "DATABASES-DEB"
	echo "$DATABASE" |\
	while read D
	do
		DB=$(echo $D | cut -d: -f1)
		LOGIN=$(echo $D | cut -d: -f2)
		TNS=$(echo $D | cut -d: -f3)
		#echo " => $DB / $LOGIN / $TNS "
		log "${DB}-DEB"
		get_DB "$D"
		log "${DB}-FIN"
	done
	log "DATABASES-FIN"
}

## ==================
## GET_DATA => DEBUT
## ==================
log "GETDATA-DEB"
export DATABASES=""
get_conf

entete
serveurs
databases

log "GETDATA-FIN"
