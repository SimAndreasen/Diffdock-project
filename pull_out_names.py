import json
import xml.etree.ElementTree as ET

def save_dict(file_name, dictionary):
    with open(f"/data_output/info_on_ipr/{file_name}.json", "w") as file:
        json.dump(dictionary, file)

input_destination = "/data_output/IPR_counts.json"

with open(input_destination, "r") as file:
    data = json.load(file)

sorted_data = dict(sorted(data.items(), key=lambda item: item[1]))
sorted_keys =  sorted_data.keys()

xml_file_location = "/interpro.xml/interpro.xml"

tree = ET.parse(xml_file_location)

root = tree.getroot()

name_dict = {}
count_dict = {}
type_dict = {}
child_dict = {}
parent_dict = {}

for elem in root.iter("interpro"):
    IPR_id = elem.attrib["id"]
    name_dict[IPR_id] = elem.find("name").text
    count_dict[IPR_id] = int(elem.attrib["protein_count"])
    type_dict[IPR_id] = elem.attrib["type"]
    child_list = []
    parent_list = []
    try:
        for item in elem.find("child_list").iter("rel_ref"):
            child_list.append(item.attrib["ipr_ref"])
    except AttributeError:
        pass
    try:
        for item in elem.find("parent_list").iter("rel_ref"):
            parent_list.append(item.attrib["ipr_ref"])
    except AttributeError:
        pass
    child_dict[IPR_id] = child_list
    parent_dict[IPR_id] = parent_list

save_dict("name_dict",name_dict)
save_dict("count_dict",count_dict)
save_dict("type_dict",type_dict)
save_dict("child_dict",child_dict)
save_dict("parent_dict",parent_dict)
save_dict("parent_dict",parent_dict)
