import json
import matplotlib.pyplot as plt

input_destination = "C:/Users/Simon/Desktop/Bachelor/data_output/IPR_counts.json"

with open(input_destination, "r") as file:
    data = json.load(file)


sorted_data = dict(sorted(data.items(), key=lambda item: item[1]))
sorted_keys =  list(sorted_data.keys())
sorted_values = list(sorted_data.values())

name_dict_dest = "C:/Users/Simon/Desktop/Bachelor/data_output/info_on_ipr/name_dict.json"



with open(name_dict_dest, "r") as file:
    keys_to_names = json.load(file)

sorted_names = []

for key in sorted_keys:
    try:
        sorted_names.append(keys_to_names[key])
    except KeyError:
        sorted_names.append(key)

sum_values=sum(sorted_values)


sorted_percentages = [value/sum_values for value in sorted_values]

ref_counts_dest = "C:/Users/Simon/Desktop/Bachelor/data_output/info_on_ipr/count_dict.json"

with open(ref_counts_dest, "r") as file:
    ref_data = json.load(file)


ids = sorted_keys[-30:]
sum_ref = sum(ref_data.values())
ref_values = [ref_data[key] for key in ids]
ref_percentages = [value/sum_ref for value in ref_values]
print(ref_percentages)

bars = sorted_names[-30:]
values = sorted_percentages[-30:]
alt_values = ref_percentages
print(bars)
print(values)
# Create bar plot
fig, ax = plt.subplots()
bar_containers = ax.bar(range(1,31), values, color='skyblue')

for bar, bar_name, red_line_val in zip(bar_containers, bars, alt_values):
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width() / 2, 0,  # y-coordinate set to 0
            bar_name,
            ha='center', va='bottom',  # vertically align to the bottom
            color='black', fontsize=8, weight='bold', rotation=90)

    ax.hlines(red_line_val, bar.get_x(), bar.get_x() + bar.get_width(), colors='red', linewidth=2)


plt.title("")
plt.show()
