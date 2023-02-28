import os
from PIL import Image
import imagehash
import shutil

# Set the path to the folder containing the images
folder_path = "/home/wot-het/duplicate image/img"

# Set the similarity threshold (0.0 to 1.0)
similarity_threshold = 0.85

# Create a dictionary to store the hashes and file paths of images
image_dict = {}

# Set the path to the folder for duplicates
duplicate_folder_path = os.path.join("/home/wot-het/duplicate image/", "duplicates")
if not os.path.exists(duplicate_folder_path):
    os.mkdir(duplicate_folder_path)

# Iterate through all the files in the folder
for file_name in os.listdir(folder_path):
    file_path = os.path.join(folder_path, file_name)

    # Check if the file is an image
    try:
        image = Image.open(file_path)
    except:
        continue

    # Generate a perceptual hash of the image
    image_hash = str(imagehash.phash(image))

    # Compare the hash to the hashes of other images in the dictionary
    is_duplicate = False
    for hash_key in image_dict.keys():
        similarity = 1 - (imagehash.hex_to_hash(image_hash) - imagehash.hex_to_hash(hash_key)) / 64
        if similarity >= similarity_threshold:
            is_duplicate = True
            shutil.move(file_path, os.path.join(duplicate_folder_path, file_name))
            break

    # Add the hash and file path to the dictionary if it's not a duplicate
    if not is_duplicate:
        image_dict[image_hash] = file_path

print("Similar images moved to 'duplicates' folder successfully!")
