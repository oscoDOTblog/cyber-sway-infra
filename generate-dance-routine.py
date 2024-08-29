import json
import boto3
import cv2
import os

# Initialize AWS clients
bedrock_runtime = boto3.client('bedrock-runtime')

# Define the preprocess_frame function
def preprocess_frame(frame, target_size=(256, 256)):
    """
    Preprocess the frame by resizing it to a fixed size.
    
    Args:
        frame (numpy.ndarray): The input frame.
        target_size (tuple): The target size for resizing the frame.
        
    Returns:
        numpy.ndarray: The preprocessed frame.
    """
    return cv2.resize(frame, target_size)

# Open the local video file
video = cv2.VideoCapture('data/pump.mp4')

# Initialize the result array
dance_sequence = []

# Process each frame of the video
while True:
    ret, frame = video.read()
    if not ret:
        break

    # Preprocess the frame (resize to 256x256)
    preprocessed_frame = preprocess_frame(frame)

    # Send the preprocessed frame to the AWS Bedrock Pose Estimation model
    response = bedrock_runtime.detect_pose(
        ModelId='aws-bedrock-pose-estimation',
        Image=preprocessed_frame
    )

    # Extract the keypoints from the model response
    keypoints = extract_keypoints(response)

    # Reformat the keypoints to match the required format
    reformatted_keypoints = {
        "leftFoot": keypoints["keypoints"][27],
        "rightFoot": keypoints["keypoints"][28],
        "head": keypoints["keypoints"][0],
        "leftHand": keypoints["keypoints"][15],
        "rightHand": keypoints["keypoints"][16]
    }

    # Append the keypoints to the dance sequence
    dance_sequence.append(reformatted_keypoints)

# Write the dance sequence to a local JSON file
with open('results.json', 'w') as f:
    json.dump(dance_sequence, f)
