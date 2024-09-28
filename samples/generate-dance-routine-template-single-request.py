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

# Read and encode the image
image_path = 'results/pump/000000.jpg'
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

# Save the response as a JSON file
with open('result.json', 'w', encoding='utf-8') as file:
    json.dump(output_json, file, ensure_ascii=False, indent=4)

print("Response saved to result.json")
