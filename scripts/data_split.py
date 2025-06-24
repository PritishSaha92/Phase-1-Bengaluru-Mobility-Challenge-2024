# script to split data into train, validation, and test sets

import os
import shutil
import random
from glob import glob
import argparse

def move_files(files, set_name, labels_folder, output_dir):
    images_out_dir = os.path.join(output_dir, set_name, 'images')
    labels_out_dir = os.path.join(output_dir, set_name, 'labels')
    os.makedirs(images_out_dir, exist_ok=True)
    os.makedirs(labels_out_dir, exist_ok=True)

    for file in files:
        # Move the image
        shutil.copy(file, images_out_dir)

        # Check if the corresponding label exists
        base_name = os.path.splitext(os.path.basename(file))[0]
        label_file = os.path.join(labels_folder, base_name + '.txt')

        if os.path.exists(label_file):
            shutil.copy(label_file, labels_out_dir)


def main(images_folder, labels_folder, output_dir, train_ratio, valid_ratio, test_ratio):
    # Get all image file paths
    image_files = glob(os.path.join(images_folder, '*.jpg'))  # Adjust if not .jpg

    if not image_files:
        print(f"No .jpg images found in {images_folder}")
        return

    # Shuffle the files
    random.shuffle(image_files)

    # Split the data
    train_split = int(train_ratio * len(image_files))
    valid_split = int(valid_ratio * len(image_files)) + train_split

    train_files = image_files[:train_split]
    valid_files = image_files[train_split:valid_split]
    test_files = image_files[valid_split:]

    # Move files to respective folders
    move_files(train_files, 'train', labels_folder, output_dir)
    move_files(valid_files, 'val', labels_folder, output_dir)
    move_files(test_files, 'test', labels_folder, output_dir)

    print("Data split completed!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Split image and label data into train, validation, and test sets.")
    parser.add_argument("--images_folder", type=str, required=True, help="Path to the folder containing images.")
    parser.add_argument("--labels_folder", type=str, required=True, help="Path to the folder containing labels.")
    parser.add_argument("--output_dir", type=str, default=".", help="Path to the output directory where train/val/test folders will be created.")
    parser.add_argument("--train_ratio", type=float, default=0.8, help="Ratio of training data.")
    parser.add_argument("--valid_ratio", type=float, default=0.1, help="Ratio of validation data.")
    # test_ratio is inferred from train and valid
    args = parser.parse_args()

    test_ratio = 1.0 - args.train_ratio - args.valid_ratio
    if test_ratio < 0:
        raise ValueError("train_ratio and valid_ratio must sum to 1.0 or less.")

    main(args.images_folder, args.labels_folder, args.output_dir, args.train_ratio, args.valid_ratio, test_ratio)
