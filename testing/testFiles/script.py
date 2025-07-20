import os
import shutil

# Define base directory
base_dir = "/home/parrot/Desktop/fyp/testFiles/c-test-suite"
output_dir = "/home/parrot/Desktop/fyp/testFiles/collected_c_files"

# Ensure output directory exists
os.makedirs(output_dir, exist_ok=True)

# Dictionary to track filenames
file_count = {}

for root, dirs, files in os.walk(base_dir):
    if os.path.basename(root) == "src":  # Only process 'src' folders
        for file in files:
            if file.endswith(".c"):
                src_path = os.path.join(root, file)

                # Handle duplicate filenames
                if file in file_count:
                    file_count[file] += 1
                    filename, ext = os.path.splitext(file)
                    new_filename = f"{filename}_{file_count[file]}{ext}"
                else:
                    file_count[file] = 1
                    new_filename = file

                dest_path = os.path.join(output_dir, new_filename)
                shutil.copy2(src_path, dest_path)
                print(f"Copied: {src_path} -> {dest_path}")

print("All .c files collected successfully!")
