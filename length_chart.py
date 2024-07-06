import matplotlib.pyplot as plt

input_destination = "data_output/length_counts.json"

with open(input_destination, "r") as file:
    data = json.load(file)

numberline= list(range(1,1000))
ordered_values = []
for number in numberline:
    if str(number) in data:
        ordered_values.append(data[str(number)])
    else:
        ordered_values.append(0)

plt.bar(numberline, ordered_values)

plt.title('Amino acid length distribution')
plt.xlabel('length')
plt.ylabel('Amounts')

# Display the chart
plt.show()
