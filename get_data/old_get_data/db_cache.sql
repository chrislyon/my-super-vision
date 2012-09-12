
COLUMN size_for_estimate FORMAT 999999999999 HEADING 'Cache Size (MB)' 
COLUMN buffers_for_estimate FORMAT 999999999999 HEADING 'Buffers' 
COLUMN estd_physical_read_factor FORMAT 990.90 HEADING 'Estd Phys|Read Factor' 
COLUMN estd_physical_reads FORMAT 999999999999 HEADING 'Estd Phys| Reads'

SELECT
	size_for_estimate,
	size_factor, 
	buffers_for_estimate, 
	estd_physical_read_factor, 
	estd_physical_reads 
FROM 
	v$db_cache_advice 
WHERE 
	name = 'DEFAULT' 
AND 
	block_size = 
	(
		SELECT value FROM v$parameter 
		WHERE name = 'db_block_size'
	) 
AND 
	advice_status = 'ON';
