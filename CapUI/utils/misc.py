import os
import numpy as np

# Generate a new filename with an index appended to it
def generate_filename_with_index(base_filename, index):
    # Split the base filename and extension
    name, ext = os.path.splitext(base_filename)
    # Concatenate the index to the name part
    new_filename = f"{name}_{index}{ext}"
    return new_filename

# Create a directory with the name of the index and save files within that directory
def save_with_indexed_directory(base_directory, index, filename, data):
    # Generate directory name with the index
    directory_name = os.path.join(base_directory, f"index_{index}")
    # Create the directory if it doesn't exist
    os.makedirs(directory_name, exist_ok=True)
    # Modify the file name
    file = generate_filename_with_index(filename, index)
    # Save the file within the directory
    file_path = os.path.join(directory_name, file)
    np.save(file_path, data)
