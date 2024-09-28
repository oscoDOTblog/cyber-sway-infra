import replicate
input = {
    "image": "https://replicate.delivery/pbxt/JUd7uI4XOs715D6Be5dhnefiAiL4tiJxeO96utZlRQxIhCpY/running2.jpeg",
    # "image": open("../results/pump/001800.jpg", "rb"),
    "show_visualisation": True
}

output = replicate.run(
    "adirik/lightweight-openpose:bc8b1d9c49a8f0942fba6bac6f864844aa55f6d1849a9260b06aaa964662cbe6",
    input=input
)

# Create a mapping of keypoint names to their coordinates
keypoints = output['json_data']['objects'][0]['keypoint_coords']
keypoint_names = output['keypoint_names']

# Create a dictionary to hold keypoint names and their coordinates
keypoint_mapping = {name: coord for name, coord in zip(keypoint_names, keypoints)}

print(keypoint_mapping)  # Output the mapping of keypoints to coordinates
#=> {'nose': [544, 159], 'neck': [549, 217], ...}

### -- keypoint_names --- ###
# nose
# neck
# right_shoulder
# right_elbow
# right_wrist
# left_shoulder
# left_elbow
# left_wrist
# right_hip
# right_knee
# right_ankle
# left_hip
# left_knee
# left_ankle
# right_eye
# left_eye
# right_ear
# left_ear