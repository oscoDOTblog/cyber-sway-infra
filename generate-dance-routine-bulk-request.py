import os
import boto3
import json
import base64

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

# Initialize an empty list to store the encoded images
encoded_images = []

# Iterate over the images in the directory and encode them
for filename in os.listdir(image_dir):
    if filename.endswith('.jpg') or filename.endswith('.png'):
        image_path = os.path.join(image_dir, filename)
        with open(image_path, 'rb') as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode()
            encoded_images.append({
                'filename': filename,
                'encoded_image': encoded_image
            })

# Prepare the payload
payload = {
    "messages": [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "Explain these AWS architecture diagrams."
                }
            ]
        }
    ],
    "max_tokens": 10000,
    "anthropic_version": "bedrock-2023-05-31",
    "images": [
        {
            "type": "image",
            "source": {
                "type": "base64",
                "media_type": "image/jpeg",
                "data": image['encoded_image']
            }
        } for image in encoded_images
    ]
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

# Save the results as a JSON file
results = []
for i, image in enumerate(encoded_images):
    result = {
        'filename': image['filename'],
        'response': output_json['content'][i]
    }
    results.append(result)

with open('result.json', 'w', encoding='utf-8') as file:
    json.dump(results, file, ensure_ascii=False, indent=4)

print("Results saved to result.json")
