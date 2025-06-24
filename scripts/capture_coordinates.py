# script to capture coordinates of turning boxes

import cv2
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Capture coordinates from an image by clicking on it.")
    parser.add_argument("image_path", help="Path to the image file.")
    args = parser.parse_args()

    # Load the image
    re_image = cv2.imread(args.image_path)

    if re_image is None:
        print(f"Error: Could not read the image from path: {args.image_path}")
        exit()

    # Store coordinates in a list
    coordinates = []
    sets_of_coordinates = []

    image = cv2.resize(re_image, (1440, 810))

    # Function to capture mouse click events
    def click_event(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            # Add coordinates to the list
            coordinates.append((x, y))
            
            # Display the coordinates on the image
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(image, str((x, y)), (x, y), font, 0.5, (255, 0, 0), 2)
            cv2.imshow('image', image)
            
            # Check if we have captured 4 points
            if len(coordinates) == 4:
                print("Captured Coordinates:", coordinates)
                sets_of_coordinates.append(coordinates.copy())
                # Clear the list for the next set of coordinates
                coordinates.clear()

    # Display the image and set mouse callback
    cv2.imshow('image', image)
    cv2.setMouseCallback('image', click_event)

    # Wait until any key is pressed
    cv2.waitKey(0)

    # Destroy all windows
    cv2.destroyAllWindows()

    # Print all sets of coordinates
    print("\nAll sets of captured coordinates:")
    for i, coord_set in enumerate(sets_of_coordinates, 1):
        print(f"'J{i}': {coord_set},")