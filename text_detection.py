from paddleocr import PaddleOCR
import cv2
import os
import glob

# Initialize PaddleOCR
ocr = PaddleOCR(lang='ch')

for image_path in glob.glob("datasets/original_image/processed_image/*.jpg"):
    image_name = os.path.basename(image_path)
    # Load the image
    image = cv2.imread(image_path)

    # Perform text detection
    result = ocr.ocr(image, det=True)

    # Create a directory to save cropped text images
    output_dir = 'cropped_text_images'
    os.makedirs(output_dir, exist_ok=True)

    # Process the detected text regions
    for detection_result in result[0][1]:
        # Get the coordinates of the detected text box
        coordinates = detection_result[0]

        # Crop the detected text region from the original image
        x1, y1, x2, y2 = coordinates
        cropped_text = image[y1:y2, x1:x2]

        # Save the cropped text as individual images
        output_path = os.path.join(output_dir, f'cropped_text_{coordinates}.png')
        cv2.imwrite(output_path, cropped_text)