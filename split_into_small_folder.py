# import os
# import shutil
# import glob

# def split_images_into_folders(source_folder, destination_folder, images_per_folder):
#     # Create the destination folder if it doesn't exist
#     if not os.path.exists(destination_folder):
#         os.makedirs(destination_folder)

#     # Get a list of all image files in the source folder
#     image_files = glob.glob(os.path.join(source_folder, '*.jpg'))  # Adjust the file extension as needed

#     # Calculate the number of folders needed
#     num_folders = (len(image_files) + images_per_folder - 1) // images_per_folder

#     for i in range(num_folders):
#         # Create subfolders in the destination folder
#         subfolder_path = os.path.join(destination_folder, f'folder_{i + 1}')
#         os.makedirs(subfolder_path)

#         # Calculate the range of images for the current subfolder
#         start_index = i * images_per_folder
#         end_index = min((i + 1) * images_per_folder, len(image_files))

#         # Copy images to the current subfolder
#         for j in range(start_index, end_index):
#             shutil.copy(image_files[j], subfolder_path)

# if __name__ == "__main__":
#     source_folder = "../datasets/pdf_extracted_vi/"  # Replace with the path to your source folder
#     destination_folder = "../datasets/"  # Replace with the path to your destination folder
#     images_per_folder = 11951

#     split_images_into_folders(source_folder, destination_folder, images_per_folder)


import os
import shutil

def merge_images_from_folders(source_folders, destination_folder):
    # Create the destination folder if it doesn't exist
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    # Iterate through the source folders
    for source_folder in source_folders:
        # Get a list of all image files in the current source folder
        image_files = [f for f in os.listdir(source_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]

        # Iterate through the image files and copy them to the destination folder
        for image_file in image_files:
            source_path = os.path.join(source_folder, image_file)
            destination_path = os.path.join(destination_folder, image_file)

            # Use shutil.copy to copy the image file
            shutil.copy(source_path, destination_path)

if __name__ == "__main__":
    # Replace these paths with the paths to your folders
    source_folders = ["D:/dev/datasets/cropped_text_images_1", "D:/dev/datasets/cropped_text_images_2", "D:/dev/datasets/cropped_text_images_3",
                      "D:/dev/datasets/cropped_text_images_4", "D:/dev/datasets/cropped_text_images_5", "D:/dev/datasets/cropped_text_images_6"]
    destination_folder = "D:/dev/datasets/cropped_image"

    merge_images_from_folders(source_folders, destination_folder)
