import os
root_image_path = "D:\dev\datasets\kethon_khaisinh"

input_file_path = "D:\dev\datasets\kethon_khaisinh.txt"
output_file_path = "new_kethon_khaisinh.txt"

# Lists to store lines for output and image paths for deletion
output_lines = []
image_paths_to_delete = []

with open(input_file_path, 'r', encoding='utf-8') as file:
    for line in file:
        # Remove leading and trailing whitespaces, then split the line by tab character
        image_path, text = map(str.strip, line.split('\t'))

        # Check if text is empty
        if text:
            # If text is not empty, add the line to the output
            output_lines.append(line)
        else:
            # If text is empty, add the image path to the list for deletion
            image_paths_to_delete.append(image_path)

# Write the lines with non-empty text to the new file
with open(output_file_path, 'w', encoding='utf-8') as output_file:
    output_file.writelines(output_lines)

# Delete images corresponding to lines with empty text
for image_path in image_paths_to_delete:
    if os.path.exists(os.path.join(root_image_path, image_path)):
        os.remove(os.path.join(root_image_path, image_path))
