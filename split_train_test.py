import os
import shutil
import random
from pathlib import Path

# Define paths
images_folder = 'images'
data_server_folder = 'data_server'
train_images_folder = 'train_images'
test_images_folder = 'test_images'
train_output_file_path = 'train.txt'
test_output_file_path = 'test.txt'

# Split ratio
split_ratio = 0.8

# Create train and test folders if they don't exist
os.makedirs(train_images_folder, exist_ok=True)
os.makedirs(test_images_folder, exist_ok=True)

# Function to format path
def format_path(path):
    return path.replace('\\', '/')

# Collect all data
data = []
for image_file in os.listdir(images_folder):
    image_path = os.path.join(images_folder, image_file)
    image_path_formatted = format_path(image_path)

    basename = Path(image_file).stem
    text_file_path = os.path.join(data_server_folder, basename + '.txt')
    text_file_path_formatted = format_path(text_file_path)

    if os.path.exists(text_file_path):
        with open(text_file_path, 'r', encoding='utf-8') as text_file:
            text_content = text_file.read().strip()
        data.append((image_path, text_file_path_formatted, image_path_formatted, text_content))
    else:
        print(f"Text file for {image_path} not found.")

# Shuffle the data
random.shuffle(data)

# Split the data
split_index = int(len(data) * split_ratio)
train_data = data[:split_index]
test_data = data[split_index:]

# Function to process and save data
def save_data(data, images_folder, output_file_path):
    with open(output_file_path, 'w', encoding='utf-8') as file:
        for image_path, text_file_path, image_path_formatted, text_content in data:
            new_image_path = os.path.join(images_folder, os.path.basename(image_path))
            new_image_path_formatted = format_path(new_image_path)
            shutil.copy(image_path, new_image_path)
            file.write(f"{new_image_path_formatted}\t{text_content}\n")

# Save train and test data
save_data(train_data, train_images_folder, train_output_file_path)
save_data(test_data, test_images_folder, test_output_file_path)
