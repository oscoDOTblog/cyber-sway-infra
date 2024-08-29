import cv2
import os
from pathlib import Path
from tqdm import tqdm

def extract_frames(video_path, output_dir, frames_per_second=30):
    print(f"Starting frame extraction process for: {video_path}")
    
    # Open the video file
    video = cv2.VideoCapture(video_path)
    
    # Get video properties
    fps = video.get(cv2.CAP_PROP_FPS)
    frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    
    # Handle cases where FPS might be reported as 0
    if fps <= 0:
        print("Warning: Video FPS reported as 0 or less. Setting to 30 FPS.")
        fps = 30
    
    duration = frame_count / fps
    
    print(f"Video Information:")
    print(f"- Duration: {duration:.2f} seconds")
    print(f"- Total frames: {frame_count}")
    print(f"- FPS: {fps:.2f}")
    print(f"- Target extraction rate: {frames_per_second} frames per second")
    
    # Calculate frame interval, ensuring it's at least 1
    interval = max(1, int(fps / frames_per_second))
    estimated_frames = frame_count // interval
    
    print(f"Estimated frames to extract: {estimated_frames}")
    
    # Create output directory
    video_name = Path(video_path).stem
    output_path = Path(output_dir) / video_name
    output_path.mkdir(parents=True, exist_ok=True)
    
    saved_count = 0
    
    # Create progress bar
    with tqdm(total=frame_count, unit='frames') as pbar:
        for frame_number in range(frame_count):
            ret, frame = video.read()
            if not ret:
                break
            
            if frame_number % interval == 0:
                output_file = output_path / f"{frame_number:06d}.jpg"
                cv2.imwrite(str(output_file), frame)
                saved_count += 1
            
            pbar.update(1)
    
    video.release()
    print(f"Frame extraction completed. Extracted {saved_count} frames from {video_name}")
    print(f"Frames saved in: {output_path}")

# Example usage
video_path = "data/pump.mp4"
output_dir = "results"

print("Video Frame Extractor")
print("--------------------")
extract_frames(video_path, output_dir, frames_per_second=1)
print("Process completed!")