import os
import json
import math
from enum import Enum
from typing import List, Tuple

import cv2
import numpy as np
import mediapipe as mp
from tqdm import tqdm
from pydub import AudioSegment  # Importing AudioSegment for audio extraction

BASE_OUTPUT_DIR = "results"
EXIST_FLAG = "-n"  # ignore existing file, change to -y to always overwrite
FPS_ANNOTATE = 24.0
GENERATE_OUTPUT_VIDEO = False  # Set to False to skip generating the output video
VIDEO_PATH = "data/caffeinated.mp4"  # Replace this with the actual path to your video

# MediaPipe setup
mp_draw = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

class PoseLandmark(Enum):
    NOSE = 0  # 0
    LEFT_SHOULDER = 11  # 1
    RIGHT_SHOULDER = 12  # 2
    LEFT_ELBOW = 13  # 3
    RIGHT_ELBOW = 14  # 4
    LEFT_WRIST = 15  # 5
    RIGHT_WRIST = 16  # 6
    LEFT_HIP = 23  # 7
    RIGHT_HIP = 24  # 8
    LEFT_KNEE = 25  # 9
    RIGHT_KNEE = 26  # 10
    LEFT_ANKLE = 27  # 11
    RIGHT_ANKLE = 28  # 12

def get_frame_count(filename: str) -> Tuple[cv2.VideoCapture, int]:
    """Returns a tuple of (captured video, frame count)."""
    video = cv2.VideoCapture(filename)
    frame_count = int(math.floor(video.get(cv2.CAP_PROP_FRAME_COUNT)))
    return video, frame_count

def extract_landmarks(video_path: str) -> Tuple[List[List[Tuple[float, float]]], List[np.ndarray], List]:
    """Extracts pose landmarks from a video."""
    pose = mp_pose.Pose()
    xy_landmark_coords = []
    frames = []
    landmarks = []

    video, frame_count = get_frame_count(video_path)

    # Create a progress bar
    pbar = tqdm(total=frame_count, desc="Extracting landmarks", unit="frame")

    for _ in range(frame_count):
        success, image = video.read()
        if not success:
            break
        frames.append(image)
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        results = pose.process(image_rgb)
        landmarks.append(results)

        if results.pose_landmarks:
            xy_landmark_coords.append([(lm.x - 0.5, 1 - lm.y) for lm in results.pose_landmarks.landmark])  # Adjusted x value
        else:
            xy_landmark_coords.append([(0, 0)] * len(PoseLandmark))

        pbar.update(1)

    pbar.close()
    return xy_landmark_coords, frames, landmarks

def extract_audio(video_path: str, output_dir: str):
    """Extracts audio from the video and saves it as an MP3 file."""
    audio = AudioSegment.from_file(video_path)  # Load the video file
    audio_output_path = os.path.join(output_dir, os.path.splitext(os.path.basename(video_path))[0] + '.mp3')
    audio.export(audio_output_path, format='mp3')  # Export as MP3
    print(f"Audio extracted and saved to: {audio_output_path}")

def process_video(video_path: str):
    """Processes a single video, outputs an annotated video and a JSON file with landmark coordinates."""
    print(f"Processing video: {video_path}")

    # Create video-specific output directory
    video_name = os.path.splitext(os.path.basename(video_path))[0]
    output_dir = os.path.join(BASE_OUTPUT_DIR, video_name)
    os.makedirs(output_dir, exist_ok=True)

    # Extract landmarks, frames, and pose results
    landmarks, frames, pose_results = extract_landmarks(video_path)

    # Get video length in milliseconds using OpenCV
    video = cv2.VideoCapture(video_path)
    frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = video.get(cv2.CAP_PROP_FPS)
    video_length_ms = int((frame_count / fps) * 1000)  # Calculate length in milliseconds
    video.release()  # Release the video capture object

    # Save metadata to JSON
    metadata = {
        "frame_count": frame_count,
        "video_length_ms": video_length_ms
    }
    metadata_output_path = os.path.join(output_dir, 'metadata.json')
    with open(metadata_output_path, 'w') as metadata_file:
        json.dump(metadata, metadata_file)

    if GENERATE_OUTPUT_VIDEO:  # Check if output video should be generated
        # Prepare output video
        output_video_path = os.path.join(output_dir, 'output_annotated.mp4')
        height, width, _ = frames[0].shape
        video_writer = cv2.VideoWriter(output_video_path, cv2.VideoWriter_fourcc(*'mp4v'), FPS_ANNOTATE, (width, height))

        # Create a progress bar for frame processing
        pbar = tqdm(total=len(frames), desc="Processing frames", unit="frame")

        # Process each frame
        for frame_idx, (frame, pose_result) in enumerate(zip(frames, pose_results)):
            # Draw pose landmarks on the frame
            annotated_frame = frame.copy()
            mp_draw.draw_landmarks(annotated_frame, pose_result.pose_landmarks, mp_pose.POSE_CONNECTIONS)

            # Add frame number to the annotated frame
            cv2.putText(annotated_frame, f"Frame: {frame_idx}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            # Write the annotated frame to the output video
            video_writer.write(annotated_frame)

            # Update progress bar
            pbar.update(1)

        pbar.close()
        video_writer.release()
        print(f"Annotated video saved to: {output_video_path}")

    # Prepare JSON output
    json_output = []
    for frame_landmarks in landmarks:
        frame_data = []
        for landmark in frame_landmarks:
            frame_data.append([landmark[0], landmark[1]])  # Changed to array format
        json_output.append(frame_data)

    # Write JSON output to file
    json_output_path = os.path.join(output_dir, 'landmarks.json')
    with open(json_output_path, 'w') as json_file:
        json.dump(json_output, json_file)

    print(f"Landmark data saved to: {json_output_path}")

    # Extract audio from the video
    extract_audio(video_path, output_dir)  # Call the audio extraction function

def main():
    process_video(VIDEO_PATH)

if __name__ == "__main__":
    main()
