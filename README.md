# cyber-sway-infra
Certainly, I'd be happy to help you create a serverless framework project with Python. Let's go through the process step by step.



First, let's create a basic structure for a serverless framework project using Python. Here's a template to get you started:

```yaml
service: my-serverless-project

provider:
  name: aws
  runtime: python3.10
  stage: dev
  region: us-east-1

functions:
  hello:
    handler: src/handler.hello
    events:
      - http:
          path: hello
          method: get

plugins:
  - serverless-python-requirements

custom:
  pythonRequirements:
    dockerizePip: non-linux

```

This is a basic `serverless.yml` file that defines a serverless project. Let's break it down:

1. `service`: This is the name of your service.
2. `provider`: Specifies the cloud provider (AWS in this case) and other settings.
3. `functions`: Defines the Lambda functions in your service.
4. `plugins`: Lists any plugins you're using (in this case, for handling Python requirements).
5. `custom`: Contains custom settings for plugins.

Now, let's create a simple Python handler file:



```python
import json

def hello(event, context):
    body = {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "input": event
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response

```

This `handler.py` file contains a simple function that returns a JSON response when triggered.

To set up this project:

1. Install the Serverless Framework if you haven't already:
   ```
   npm install -g serverless
   ```

2. Create a new directory for your project and navigate into it:
   ```
   mkdir my-serverless-project
   cd my-serverless-project
   ```

3. Create the `serverless.yml` file and paste the content from the first artifact.

4. Create a `handler.py` file and paste the content from the second artifact.

5. Create a `requirements.txt` file (even if it's empty for now) for any Python dependencies.

6. Install the `serverless-python-requirements` plugin:
   ```
   npm install --save-dev serverless-python-requirements
   ```

7. Deploy your project:
   ```
   serverless deploy
   ```

This will create a basic serverless project with a single function that responds to HTTP GET requests.

Would you like me to explain any part of this setup in more detail or help you customize it further?

## Output
```json
[
  // Frame 1
  [
    [0.5, 0.1],  // NOSE
    [0.4, 0.3],  // LEFT_SHOULDER
    [0.6, 0.3],  // RIGHT_SHOULDER
    [0.3, 0.5],  // LEFT_ELBOW
    [0.7, 0.5],  // RIGHT_ELBOW
    [0.2, 0.7],  // LEFT_WRIST
    [0.8, 0.7],  // RIGHT_WRIST
    [0.45, 0.6], // LEFT_HIP
    [0.55, 0.6], // RIGHT_HIP
    [0.4, 0.8],  // LEFT_KNEE
    [0.6, 0.8],  // RIGHT_KNEE
    [0.35, 1.0], // LEFT_ANKLE
    [0.65, 1.0]  // RIGHT_ANKLE
  ],
  // Frame 2
  [
    [0.51, 0.11],
    [0.41, 0.31],
    [0.61, 0.31],
    // ... (other landmarks)
  ],
  // ... (Frames 3 to 47)
  // Frame 48
  [
    [0.53, 0.13],
    [0.43, 0.33],
    [0.63, 0.33],
    // ... (other landmarks)
  ]
]
```