# script to stream video and perform object detection for testing

import cv2
from ultralytics import YOLO
import argparse

def main(video_path, model_path):
    # Load the YOLO model
    model = YOLO(model_path)  

    # Open the video file
    cap = cv2.VideoCapture(video_path)  

    if not cap.isOpened():
        print(f"Error: Could not open video: {video_path}")
        exit()

    while cap.isOpened():
        ret, frame = cap.read()

        if not ret:
            break

        # Perform object detection
        results = model(frame)

        # Iterate over results and render each one
        for result in results:
            annotated_frame = result.plot()

        # Display the annotated frame
        cv2.imshow('YOLO Object Detection', annotated_frame)

        # Press 'q' to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the video capture object and close all OpenCV windows
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Stream a video and perform object detection using a YOLO model.")
    parser.add_argument("video_path", help="Path to the video file to be streamed.")
    parser.add_argument("--model", default="../models/best.pt", help="Path to the YOLO model file.")
    args = parser.parse_args()
    main(args.video_path, args.model)
