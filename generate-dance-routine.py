import os
import base64
import io
from typing import List, Dict
import multiprocessing
import boto3
from PIL import Image

# Initialize the boto3 client outside the function
client = boto3.client("bedrock-runtime", region_name="us-west-2")
model_id = "anthropic.claude-3-haiku-20240307-v1:0"

def process_image(args):
    image_path, prompt = args
    filename = os.path.basename(image_path)

    try:
        with Image.open(image_path) as img:
            img = img.resize((512, 512))
            img_byte_arr = io.BytesIO()
            img.save(img_byte_arr, format='JPEG')
            
            img_byte_arr = img_byte_arr.getvalue()
            base64_image = base64.b64encode(img_byte_arr).decode('utf-8')

        conversation = [
            {
                "role": "user",
                "content": [
                    {"image": base64_image},
                    {"text": prompt}
                ],
            }
        ]

        response = client.converse(
            modelId=model_id,
            messages=conversation,
            inferenceConfig={"maxTokens": 4096, "temperature": 0},
            additionalModelRequestFields={"top_k": 250}
        )

        response_text = response["output"]["message"]["content"][0]["text"]
        print(f"Successfully processed {filename}")
        return response_text

    except Exception as e:
        print(f"ERROR: Can't process '{filename}'. Reason: {e}")
        return None


def process_images(directory: str, prompt: str) -> List[Dict]:
    print(f"Beginning image processing in directory: {directory}")
    image_paths = [os.path.join(directory, filename) for filename in os.listdir(directory)
                   if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]

    pool = multiprocessing.Pool()
    results = pool.map(process_image, [(path, prompt) for path in image_paths])
    pool.close()
    pool.join()

    print(f"Image processing completed. Total images processed: {len(results)}")
    return [{"image_name": os.path.basename(path), "result": result}
            for path, result in zip(image_paths, results) if result is not None]

# Usage
directory = "results/pump"
prompt = "Estimate the x,y,z positions of the hand left, hand right, knee left, and knee right"

print("Starting the image analysis process...")
results = process_images(directory, prompt)

print("Analysis complete. Printing results:")
for result in results:
    print(result)

print("Process finished successfully.")
