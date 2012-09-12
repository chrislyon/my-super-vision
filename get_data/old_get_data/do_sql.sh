:
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
	SID=$2
	db_user=$3
	shift
	shift
	shift
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
	cat $TEMP_FILE
	su - ${user} -c ". /oracle/product/9.2.0/.profile ; export ORACLE_SID=$SID;sqlplus -S $db_user @$TEMP_FILE"
	rm -f $TEMP_FILE
}
do_sql $user $SID $db_user "@$DIR/top_sql.sql"
