import json
from Bio import Phylo
from Bio.Phylo.BaseTree import Tree, Clade


def remove_after_instance(s,number):
    parts = s.split(".")
    return ".".join(parts[:number])


ec_counts_path = "C:/Users/Simon/Desktop/Bachelor/data_output/EC_counts.json"


with open(ec_counts_path, "r") as file:
    data = json.load(file)

sorted_data = dict(sorted(data.items(), key=lambda item: item[0]))
sorted_data_keys = list(sorted_data.keys())

range_list = list(range(1,4))
range_list.reverse()
EC_ids_added_to_graph = {}
EC_ids_connected = {}
EC_ids_amount = {}


for key in sorted_data_keys:
    if key.count(".") == 3:
        EC_ids_added_to_graph[key] = True
        EC_ids_amount[key] = sorted_data[key]
        old_key = key
        for number in range_list:
            new_key = remove_after_instance(key, number)
            try:
                EC_ids_added_to_graph[new_key]
            except KeyError:
                EC_ids_added_to_graph[new_key] = True
            try:
                EC_ids_amount[new_key]
            except KeyError:
                try:
                    EC_ids_amount[new_key] = sorted_data[new_key]
                except KeyError:
                    EC_ids_amount[new_key] = 0
            try:
                EC_ids_connected[(new_key,old_key)]
            except KeyError:
                EC_ids_connected[(new_key,old_key)] = True

            old_key = new_key

list_of_ec_ids = sorted(list(EC_ids_added_to_graph.keys()))
EC_ids_added_up = dict(sorted(EC_ids_amount.items(), key=lambda item: item[0]))
for number in range_list:
    for ec_id in list_of_ec_ids:
        if ec_id.count(".") == number:
            parent_id = remove_after_instance(ec_id,number)
            EC_ids_added_up[parent_id] = EC_ids_added_up[parent_id] + EC_ids_added_up[ec_id]
filtered_EC_ids_added_up = {k: v for k, v in EC_ids_added_up.items() if v >= 100}
print(filtered_EC_ids_added_up)
nodes = sorted(list(filtered_EC_ids_added_up.keys()))
edges = list(EC_ids_connected.keys())

nodes.append('Root')
for number in range(1,8):
    edges.append(("Root",str(number)))
print(nodes)
print(edges)


valid_edges = [(parent, child) for parent, child in edges if parent in nodes and child in nodes]

# Create a mapping of node name to Clade
clade_map = {name: Clade(name=name) for name in nodes}

# Connect nodes based on valid edges
for parent, child in valid_edges:
    clade_map[parent].clades.append(clade_map[child])

# Create a tree
tree = Tree(clade_map['Root'])

# Display the tree
Phylo.draw(tree)