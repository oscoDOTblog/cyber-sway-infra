import json

# Read the input JSON file
with open('result.json', 'r') as file:
    data = json.load(file)

# Extract and parse the JSON strings from each response
master_array = []
for index, item in enumerate(data):
    try:
        json_string = item['response']['content'][0]['text']
        parsed_json = json.loads(json_string)
        # Add the frame number to the parsed JSON
        parsed_json['frame'] = index
        master_array.append(parsed_json)
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON for item {index}: {e}")
        print(f"Problematic content: {json_string}")
    except KeyError as e:
        print(f"KeyError for item {index}: {e}")
        print(f"Item structure: {item}")

# Write the master array to a new JSON file
with open('master_result.json', 'w') as outfile:
    json.dump(master_array, outfile, indent=2)

print(f"Master JSON file 'master_result.json' has been created with {len(master_array)} valid items.")