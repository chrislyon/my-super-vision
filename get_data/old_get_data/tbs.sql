col tablespace_name   format a30         head "Tablespace" 
col taille            format 999999999  head "Taille|(en Mo)" 
col libre             format 999999999  head "Disponible|(en Mo)" 
col pctf              format 990         head "%|free" 
break on report 
compute sum of taille libre on report 
compute avg of pctf on report 
SELECT 
   a.tablespace_name tablespace_name , 
   100-(100-round(b.total_bytes*100/sum(c.user_bytes),2)) pctf, 
   (round(b.total_bytes/1024/1024,2)) libre, 
   (round(sum(c.bytes)/1024/1024,2)) taille 
FROM 
   dba_tablespaces a, 
   dba_data_files c, 
   dba_free_space_coalesced b  
WHERE 
   a.tablespace_name = b.tablespace_name 
AND 
   c.tablespace_name = a.tablespace_name 
GROUP BY 
   a.tablespace_name, 
   a.status, 
   a.contents, 
   a.allocation_type, 
   b.percent_extents_coalesced, 
   b.total_extents, 
   b.total_bytes 
ORDER BY 1 ; 

clear breaks 
clear compute
