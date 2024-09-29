import time 
from PIL import Image  # Import the PIL library
import json  # Import the json module for handling JSON data

from gradio_client import Client, handle_file

client = Client("facebook/sapiens-pose") # Original model
#client = Client("TimeInverse/sapiens-pose") # Custom model

# Start timing
start_time = time.time()  

result = client.predict(
		# image=handle_file('https://huggingface.co/spaces/facebook/sapiens-pose/resolve/main/assets/images/pexels-gabby-k-6311686.png'),
		image=handle_file("../results/pump/001800.jpg"),
        model_name="0.3b",
		kpt_threshold="0.3",
		api_name="/process_image"
)

elapsed_time = time.time() - start_time  # Calculate elapsed time

# Update print statement to reflect result indices and elapsed time
filepath_img = result[0]  # Assuming result[0] is the image file path
filepath_json = result[1]  # Assuming result[1] is the JSON file path
print(f"Image saved at: {filepath_img}")
print(f"JSON data at: {filepath_json}")
print(f"Time elapsed: {elapsed_time:.2f} seconds")

# Load the JSON data from the specified file
with open(filepath_json, 'r') as file:  # Load JSON after prediction
    result_json = json.load(file)

# Open the image to get its height
image_path = "../results/pump/001800.jpg"
with Image.open(image_path) as img:
    height = img.height  # Get the height of the image

# Update y values in the JSON data
for item in result_json:  # Iterate through the list of dictionaries
    for key in item:
        if isinstance(item[key], list) and len(item[key]) > 1:
            item[key][1] = height - item[key][1]  # Update y value

# Write the updated JSON data to a new file
updated_json_file_path = filepath_json.replace('.json', '_updated.json')
with open(updated_json_file_path, 'w') as file:
    json.dump(result_json, file, indent=4)  # Save the updated JSON data

print(f"Updated JSON data saved to: {updated_json_file_path}")  # Print the path of the updated file