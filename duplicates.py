import os
import hashlib

def calculate_file_hash(file_path, hash_algo="sha256"):
    """
    Calculate the hash of a file.
    
    Args:
        file_path (str): Path to the file.
        hash_algo (str): Hash algorithm (default is "sha256").
    
    Returns:
        str: The file's hash.
    """
    hash_obj = hashlib.new(hash_algo)
    with open(file_path, "rb") as file:
        while chunk := file.read(4096):
            hash_obj.update(chunk)
    return hash_obj.hexdigest()

def find_duplicate_files(directory):
    """
    Find and list files with matching hashes in a directory.

    Args:
        directory (str): The directory to search for duplicate files.

    Returns:
        dict: A dictionary where keys are file hashes and values are lists of colliding file paths.
    """
    file_hash_dict = {}
    for root, _, files in os.walk(directory):
        for filename in files:
            file_path = os.path.join(root, filename)
            file_hash = calculate_file_hash(file_path)
            if file_hash in file_hash_dict:
                file_hash_dict[file_hash].append(file_path)
            else:
                file_hash_dict[file_hash] = [file_path]
    
    # Filter out hashes with only one file (no duplicates)
    duplicate_files = {hash_val: paths for hash_val, paths in file_hash_dict.items() if len(paths) > 1}
    return duplicate_files

DIRECTORY_TO_SEARCH = ''

if __name__ == "__main__":
    directory_to_search = "/Volumes/NetBackup/Media/audio"
    duplicate_files = find_duplicate_files(directory_to_search)
    
    if duplicate_files:
        for hash_val, file_paths in duplicate_files.items():
            print(f"Hash: {hash_val}")
            for file_path in file_paths:
                print(f"  - {file_path}")
    else:
        print("No duplicate files found.")
