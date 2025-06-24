import os
import shutil
import argparse

def combine_folders(source_folders, destination_folder):
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)
    
    for folder in source_folders:
        for root, dirs, files in os.walk(folder):
            relative_path = os.path.relpath(root, folder)
            dest_path = os.path.join(destination_folder, relative_path)
            
            if not os.path.exists(dest_path):
                os.makedirs(dest_path)
            
            for file in files:
                src_file = os.path.join(root, file)
                dest_file = os.path.join(dest_path, file)
                if not os.path.exists(dest_file):
                    shutil.copy2(src_file, dest_file)
                else:
                    base, extension = os.path.splitext(file)
                    counter = 1
                    new_dest_file = os.path.join(dest_path, f"{base}_{counter}{extension}")
                    while os.path.exists(new_dest_file):
                        counter += 1
                        new_dest_file = os.path.join(dest_path, f"{base}_{counter}{extension}")
                    shutil.copy2(src_file, new_dest_file)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Combine multiple data folders into a single destination folder.")
    parser.add_argument("source_folders", nargs='+', help="List of source folders to combine.")
    parser.add_argument("destination_folder", help="The destination folder to store the combined data.")
    args = parser.parse_args()

    combine_folders(args.source_folders, args.destination_folder)
