import boto3
import json

s3 = boto3.client('s3')
bedrock_runtime = boto3.client(service_name="bedrock-runtime")

SDXL_MODEL_ID = 'stability.stable-diffusion-xl-v1'

def lambda_handler(event, context):
    # Get the text prompt from the API request body
    body = json.loads(event['body'])
    prompt = body.get('prompt')

    # Prepare the request payload for the SDXL 1.0 model
    payload = {
        'text_prompts': [{'text': prompt}],
        'seed': 42,  # You can use a different seed value
        'style_preset': 'photographic'  # You can use a different style preset
    }

    # Invoke the SDXL 1.0 model
    response = bedrock_runtime.invoke_model(
        modelId=SDXL_MODEL_ID,
        body=json.dumps(payload)
    )

    # Handle the response from the model
    print(response.keys())
    image_data = response['body'].read().decode('utf-8')
    # Upload the generated image to Amazon S3
    key = f'generated-image.png'

    return {
        'statusCode': 200,
        'body': json.dumps({'data':image_data,'name':key}),
        'headers': {
            'Access-Control-Allow-Origin': '*'
        }
    }


if __name__ == '__main__':
    # Test case 1: Valid prompt
    event = {
        'body': json.dumps({'prompt': 'A beautiful sunset over the ocean'})
    }
    context = {}
    response = lambda_handler(event, context)
    print(f"Test case 1 response: {response}")