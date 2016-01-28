SELECT

max(activities.activity_id),
component_sequences.accession AS uniprot_accession,
molecule_dictionary.chembl_id AS mol_chembl_id,
avg(activities.standard_value),
max(activities.standard_relation),
max(activities.standard_type),
max(assays.assay_type),
max(assays.confidence_score)

FROM

compound_properties
INNER JOIN molecule_dictionary USING(molregno)
INNER JOIN compound_structures USING(molregno)
INNER JOIN activities USING(molregno)
INNER JOIN assays USING(assay_id)
INNER JOIN target_dictionary USING(tid)
INNER JOIN target_components USING(tid)
INNER JOIN component_sequences USING(component_id)

WHERE

activities.standard_value IS NOT NULL AND
activities.standard_units = 'nM' AND
activities.standard_type IN ('Kd','AC50', 'Potency', 'XC50', 'IC50', 'Ki', 'EC50') AND
activities.standard_relation IN ('=','>','<','<=','>=') AND

molecule_dictionary.structure_type = 'MOL' AND
molecule_dictionary.molecule_type = 'Small molecule' AND
compound_properties.mw_freebase < 900 AND
compound_properties.heavy_atoms > 3 AND
molecule_dictionary.inorganic_flag = -1 AND
molecule_dictionary.polymer_flag = 0

GROUP BY component_sequences.accession, molecule_dictionary.chembl_id
;
