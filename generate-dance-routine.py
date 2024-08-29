import os
import boto3
import json
import base64
import sys

# Set your AWS credentials and region
# Uncomment and set these if not using AWS CLI configuration
# os.environ['AWS_ACCESS_KEY_ID'] = 'your_access_key_id'
# os.environ['AWS_SECRET_ACCESS_KEY'] = 'your_secret_access_key'
# os.environ['AWS_REGION'] = 'your_region'

# Instantiate a Bedrock client
bedrock_runtime_client = boto3.client('bedrock-runtime')

# Select the model ID
model_id = "anthropic.claude-3-haiku-20240307-v1:0"

# Specify the directory containing the images
image_dir = 'results/pump'

# Initialize an empty list to store the results
results = []

# Get the total number of images in the directory
image_files = [f for f in os.listdir(image_dir) if f.endswith('.jpg') or f.endswith('.png')]
total_images = len(image_files)

# Iterate over the images in the directory
for i, filename in enumerate(image_files, start=1):
    image_path = os.path.join(image_dir, filename)
    with open(image_path, 'rb') as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode()

    # Prepare the payload
    payload = {
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": "image/jpeg",
                            "data": encoded_image
                        }
                    },
                    {
                        "type": "text",
                        "text": "Explain this AWS architecture diagram."
                    }
                ]
            }
        ],
        "max_tokens": 10000,
        "anthropic_version": "bedrock-2023-05-31"
    }

    # Invoke the model
    response = bedrock_runtime_client.invoke_model(
        modelId=model_id,
        contentType="application/json",
        body=json.dumps(payload)
    )

    # Process the response
    output_binary = response["body"].read()
    output_json = json.loads(output_binary)

    # Append the result to the list
    result = {
        'filename': filename,
        'response': output_json
    }
    results.append(result)

    # Update the progress bar
    progress = (i / total_images) * 100
    remaining = 100 - progress
    sys.stdout.write(f"\rProcessing images: [{('=' * int(progress // 2))}{(' ' * int(remaining // 2))}] {progress:.2f}% remaining")
    sys.stdout.flush()

# Save the results as a JSON file
with open('result.json', 'w', encoding='utf-8') as file:
    json.dump(results, file, ensure_ascii=False, indent=4)

print("\nResults saved to result.json")
