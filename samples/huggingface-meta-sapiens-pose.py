import time  # Add this import at the top of the file

from gradio_client import Client, handle_file

client = Client("facebook/sapiens-pose")
start_time = time.time()  # Start timing

result = client.predict(
		image=handle_file('https://huggingface.co/spaces/facebook/sapiens-pose/resolve/main/assets/images/pexels-gabby-k-6311686.png'),
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
