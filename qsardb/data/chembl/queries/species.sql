SELECT
	tax_id,
	max(organism)
FROM
	component_sequences
GROUP BY
	tax_id
