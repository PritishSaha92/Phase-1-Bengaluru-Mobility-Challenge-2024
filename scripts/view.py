# Code that lets us view the turning boxes created against the actual images of the junction for easier interpretation.

import cv2
import numpy as np
import argparse
import sys
import os

# Add the parent directory to the Python path to allow imports from src
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.config import locations_config

# Function to draw bounding boxes
def draw_bounding_boxes(img, regions):
    for region_name, coord_set in regions.items():
        # Convert list to a NumPy array of points
        pts = np.array(coord_set, np.int32)
        pts = pts.reshape((-1, 1, 2))
        # Draw a closed polygon (bounding box)
        cv2.polylines(img, [pts], isClosed=True, color=(0, 255, 0), thickness=2)
        # Position the text near the top-left corner of the bounding box
        text_position = (coord_set[0][0], coord_set[0][1] - 10)
        cv2.putText(img, region_name, text_position, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Show the image with the bounding boxes
    cv2.imshow('image', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="View region bounding boxes from the config on an image.")
    parser.add_argument("image_path", help="Path to the image file.")
    parser.add_argument("camera_id", help="The Camera ID for which to display the regions.", choices=locations_config.keys())
    args = parser.parse_args()

    # Load the image
    image = cv2.imread(args.image_path)
    if image is None:
        print(f"Error: Could not read image from {args.image_path}")
        exit()

    # Resize the image if needed
    image = cv2.resize(image, (1440, 810))

    # Get regions for the specified camera ID
    regions = locations_config[args.camera_id]['regions']

    # Draw the bounding boxes on the image
    draw_bounding_boxes(image, regions)