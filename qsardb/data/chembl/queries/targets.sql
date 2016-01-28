SELECT
	accession,
	max(tax_id),
	max(sequence)
FROM
	component_sequences
WHERE
	component_type = 'PROTEIN'

GROUP BY
	accession
