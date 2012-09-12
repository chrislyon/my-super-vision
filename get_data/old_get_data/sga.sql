select '==> v$sga' from dual;
col name format a30
col value format 999999999999 
select name, value from v$sga;
select '==> v$sgastat' from dual;
col pool format 999999999
col sum(bytes) format 999999999999
select pool, sum(bytes) from v$sgastat group by pool;
