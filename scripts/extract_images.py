# script to extract images from a video at a set frame interval

import cv2
import os
import argparse

# Function to extract frames at a reduced frame rate
def extract_frames(video_path, output_folder, frame_skip):
    # Create the output directory if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Open the video file
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error: Could not open video file: {video_path}")
        return

    vid_name = os.path.splitext(os.path.basename(video_path))[0]

    frame_count = 0
    saved_frame_count = 0
    success = True

    while success:
        # Read a frame
        success, frame = cap.read()

        if success:
            # Save every nth frame
            if frame_count % frame_skip == 0:
                frame_filename = os.path.join(output_folder, f"{vid_name}_frame_{saved_frame_count:05d}.jpg")
                cv2.imwrite(frame_filename, frame)
                saved_frame_count += 1

            frame_count += 1

    # Release the video capture object
    cap.release()
    print(f"Extracted {saved_frame_count} frames to {output_folder}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract frames from a video at a set interval.")
    parser.add_argument("video_path", help="Path to the video file.")
    parser.add_argument("output_folder", help="Folder to save the extracted frames.")
    parser.add_argument("--frame_skip", type=int, default=50, help="Interval of frames to skip before saving the next one.")
    args = parser.parse_args()

    extract_frames(args.video_path, args.output_folder, args.frame_skip)
