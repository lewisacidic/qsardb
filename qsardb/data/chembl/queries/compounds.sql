SELECT
molecule_dictionary.chembl_id,
compound_structures.canonical_smiles

FROM
compound_structures
INNER JOIN molecule_dictionary USING(molregno)
INNER JOIN compound_properties USING(molregno)

WHERE
molecule_dictionary.structure_type = 'MOL' AND
molecule_dictionary.molecule_type = 'Small molecule' AND
compound_properties.mw_freebase < 900 AND
compound_properties.heavy_atoms > 3 AND
molecule_dictionary.inorganic_flag = -1 AND
molecule_dictionary.polymer_flag = 0
