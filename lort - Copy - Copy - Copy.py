import requests
from rdkit import Chem
from collections import defaultdict
import os

def get_info_from_json(response):
    try:
        return response
    except KeyError:
        return None

def formula_string_to_dict(formula_str):
    atom=""
    count=""
    formula_dict = {}
    for character in formula_str:
        if character.isalpha():
            atom += character
        elif character.isdigit():
            count += character
        elif character == " ":
            if count == "":
                formula_dict[atom] = 1
            else:
                formula_dict[atom] = int(count)
            count = ""
            atom = ""

    if count == "":
        formula_dict[atom] = 1
    else:
        formula_dict[atom] = int(count)

    #removes Hydrogen from the library for comparison reasons.
    formula_dict.pop("H", None)

    return formula_dict

def get_query(pdb_id):
    url = "https://data.rcsb.org/graphql"
    query = f"""
    {{
      entry(entry_id: "{pdb_id}") {{
        polymer_entities {{
          entity_poly{{
          rcsb_sample_sequence_length
          }}
          rcsb_polymer_entity_container_identifiers{{
            asym_ids
          }}
          uniprots{{
            rcsb_uniprot_container_identifiers{{
              uniprot_id
            }}
          }}
          rcsb_polymer_entity{{
            rcsb_enzyme_class_combined{{
              ec
            }}
          }}
          rcsb_polymer_entity_annotation {{
            annotation_id
          }} 
        }}
        nonpolymer_entities {{
          nonpolymer_comp {{
            chem_comp {{
                formula
                id
            }}
            rcsb_chem_comp_descriptor {{
              InChIKey
              SMILES
            }}
          }}
        }}
      }}
    }}
    """

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    response = requests.post(url, json={'query': query}, headers=headers)

    if response.status_code == 200:
        response_json = response.json()
        try:
            nonpolymer_entities = response_json['data']['entry']['nonpolymer_entities']
        except TypeError:
            nonpolymer_entities = None


        try:
            polymer_entities = response_json['data']['entry']['polymer_entities']
        except TypeError:
            polymer_entities = None

        if nonpolymer_entities == None:
            InChIKeys = []
            ligand_ids = []
            formula_dicts = []
            SMILES = []
        else:
            InChIKeys = []

            for entity in nonpolymer_entities:
                try:
                    InChIKeys.append(get_info_from_json(entity['nonpolymer_comp']['rcsb_chem_comp_descriptor']['InChIKey']))
                except TypeError:
                    InChIKeys.append("")
            formulas = []

            for entity in nonpolymer_entities:
                formulas.append(get_info_from_json(entity['nonpolymer_comp']['chem_comp']['formula']))

            formula_dicts = []
            for formula in formulas:
                try:
                    formula_dicts.append(formula_string_to_dict(formula))
                except TypeError:
                    formula_dicts.append({})
            ligand_ids = []

            for entity in nonpolymer_entities:
                ligand_ids.append(get_info_from_json(entity['nonpolymer_comp']['chem_comp']['id']))

            SMILES = []
            for entity in nonpolymer_entities:
                try:
                    SMILES.append(get_info_from_json(entity['nonpolymer_comp']['rcsb_chem_comp_descriptor']['SMILES']))
                except TypeError:
                    SMILES.append("")
        if polymer_entities == None:
            uniprot_ids = []
            IPR_ids = []
            Enzyme_class = []
            polymer_ids = []
            length_list = []
        else:
            IPR_ids = []
            for entity in polymer_entities:
                id_list = []
                try:
                    for ids in entity["rcsb_polymer_entity_annotation"]:
                        id_list.append(get_info_from_json(ids["annotation_id"]))
                except TypeError:
                    pass
                IPR_list = [entry for entry in id_list if entry.startswith("IPR")]
                IPR_ids.append(IPR_list)

            uniprot_ids = []
            for entity in polymer_entities:
                uniprot_list = []
                try:
                    for ids in entity["uniprots"]:
                        uniprot_list.append(ids["rcsb_uniprot_container_identifiers"]["uniprot_id"])
                except TypeError:
                    pass
                uniprot_ids.append(uniprot_list)

            Enzyme_class = []
            for entity in polymer_entities:
                class_vars=[]
                try:
                    for variations in entity["rcsb_polymer_entity"]["rcsb_enzyme_class_combined"]:
                        class_vars.append(variations["ec"])
                except TypeError:
                    pass

                Enzyme_class.append(class_vars)

            polymer_ids = []

            for entity in polymer_entities:
                polymer_ids.append(entity['rcsb_polymer_entity_container_identifiers']['asym_ids'])

            length_list = []
            for entity in polymer_entities:
                length_list.append(entity["entity_poly"]["rcsb_sample_sequence_length"])

        return uniprot_ids, IPR_ids, Enzyme_class, ligand_ids, formula_dicts, InChIKeys, polymer_ids, length_list, SMILES
    else:
        print(f"Query failed for {pdb_id} with status code {response.status_code}.")
        return [], [], [], [], [], [], [], []

def count_atoms(sdf_file):
    # Create a supplier to read the SDF file
    supplier = Chem.SDMolSupplier(sdf_file)

    # Initialize a defaultdict to count atoms
    atom_counts = defaultdict(int)

    # Iterate over all molecules in the SDF file
    for molecule in supplier:
        # Make sure the molecule is valid
        if molecule is not None:
            # Iterate over all atoms in the molecule
            for atom in molecule.GetAtoms():
                # Increase the count of this atom's type
                atom_counts[atom.GetSymbol()] += 1

    return atom_counts


def get_info(pdb_id):
    uniprot_ids, IPR_ids, Enzyme_class, ligand_ids, formula_dicts, InChIKeys, polymer_ids, length_list, SMILES =get_query(pdb_id)
    information = uniprot_ids, IPR_ids, Enzyme_class, ligand_ids, formula_dicts, InChIKeys, polymer_ids, length_list, SMILES

    output = [pdb_id, [uniprot_ids, IPR_ids, Enzyme_class, polymer_ids, length_list], [InChIKeys, formula_dicts, ligand_ids, SMILES]]
    return output

pdb_id_list_location = "C:/Users/Simon/Desktop/Bachelor/DTU_ting/their_files.txt"
pdb_id_file = open(pdb_id_list_location, "r")
pdb_id_list = pdb_id_file.read().split("\n")
pdb_id_file.close()

#pdb_id_list = ["4qqi"]



output_destination= "C:/Users/Simon/Desktop/Bachelor/data_output/output_DTU_data.txt"

output_file = open(output_destination, "a")

for pdb_id in pdb_id_list:
    output = get_info(pdb_id)
    output_str= str(output)
    print(output_str)
    output_file.write(output_str + "\n")
output_file.close()