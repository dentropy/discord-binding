import json
def count_values_recursive(dictionary):
  count = 0
  for key in dictionary:
    count += len(dictionary[key])
  return count

with open("out.json", 'r') as json_file:
  data = json.load(json_file)
number_of_values = count_values_recursive(data)
print("Number of values in the recursive dictionary:", number_of_values)