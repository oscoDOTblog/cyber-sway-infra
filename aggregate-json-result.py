import json

# Read the input JSON file
with open('result.json', 'r') as file:
    data = json.load(file)

# Extract and parse the JSON strings from each response
master_array = []
for item in data:
    json_string = item['response']['content'][0]['text']
    parsed_json = json.loads(json_string)
    master_array.append(parsed_json)

# Write the master array to a new JSON file
with open('master_result.json', 'w') as outfile:
    json.dump(master_array, outfile, indent=2)

print("Master JSON file 'master_result.json' has been created.")