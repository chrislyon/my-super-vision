col table_name format a30
col num_rows format 999999999
connect ENAP/tiger
select table_name, num_rows
from user_tables
order by 2 desc;
