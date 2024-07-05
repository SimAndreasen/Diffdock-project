import json

def doublelist_to_list(input_list):
    output_list = []
    for entity in input_list:
        for item in entity:
            output_list.append(item)

    return output_list

def add_list_to_dict(PDB_id, dictionary, list):
    for id in list:
        if id in dictionary:
            dictionary[id].append(PDB_id)
        else:
            dictionary[id] = [PDB_id]

def count_amounts_in_dict(input_dict):
    counts = {}
    for key, value in input_dict.items():
        counts[key] = len(value)
    return counts

def save_file(destination, input):
    with open(destination, "w") as file:
        json.dump(input, file)

input_destination= "/data_output/output_training_data.txt"
with open(input_destination, "r") as file:
    complex_list = file.read().split("\n")

IPR_dict ={}
EC_dict = {}
length_dict = {}

for complex_uneval in complex_list:
    complex = eval(complex_uneval)
    PDB_id = complex[0]
    print(PDB_id)
    proteins = complex[1]
    ligands = complex[2]


    IPR_list = doublelist_to_list(proteins[1])
    add_list_to_dict(PDB_id, IPR_dict, IPR_list)


    EC_list = doublelist_to_list(proteins[2])
    add_list_to_dict(PDB_id, EC_dict, EC_list)


    length_list = proteins[4]
    add_list_to_dict(PDB_id, length_dict, length_list)
    #print(length_dict)



IPR_counts = count_amounts_in_dict(IPR_dict)
EC_counts = count_amounts_in_dict(EC_dict)
length_counts = count_amounts_in_dict(length_dict)

IPR_destination= "/data_output/IPR_dict.json"
EC_destination= "/data_output/EC_dict.json"
length_destination = /data_output/length_dict.json"

IPR_counts_destination= "/data_output/IPR_counts.json"
EC_counts_destination= "/data_output/EC_counts.json"
length_counts_destination= "/data_output/length_counts.json"

save_file(IPR_destination, IPR_dict)
save_file(IPR_counts_destination, IPR_counts)
save_file(EC_destination, EC_dict)
save_file(EC_counts_destination, EC_counts)
save_file(length_destination, length_dict)
save_file(length_counts_destination, length_counts)









