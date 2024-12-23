import glob
import logging
import os
import uuid

import cv2
from paddleocr import PaddleOCR
from tqdm import tqdm

logging.basicConfig(
    filename="error.log",
    level=logging.ERROR,
    format="%(asctime)s %(levelname)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

# Initialize PaddleOCR
ocr = PaddleOCR(gpu_mem=4000)

# Create a directory to save cropped text images
output_dir = "D:\dev\datasets\cropped_original_image"
os.makedirs(output_dir, exist_ok=True)

image_files = glob.glob("D:\dev\datasets\original_image\output_image\*.jpg")

progress_bar = tqdm(total=len(image_files), desc="Processing images", unit="file")

for image_path in image_files:
    try:
        img = cv2.imread(image_path)

        # Perform text detection
        result = ocr.ocr(img, det=True, rec=False, cls=False)
        result = result[:][:][0]

        # Create Boxes
        boxes = []
        for line in result:
            boxes.append(
                [[int(line[0][0]), int(line[0][1])], [int(line[2][0]), int(line[2][1])]]
            )

        boxes = boxes[::-1]

        EXPEND = 5
        for box in boxes:
            box[0][0] = box[0][0] - EXPEND
            box[0][1] = box[0][1] - EXPEND
            box[1][0] = box[1][0] + EXPEND
            box[1][1] = box[1][1] + EXPEND

        texts = []
        for box in boxes:
            cropped_image = img[box[0][1] : box[1][1], box[0][0] : box[1][0]]
            random_filename = str(uuid.uuid4())[:8]
            output_path = os.path.join(
                output_dir,
                f"cropped_text_{random_filename}.jpg",
            )
            cv2.imwrite(output_path, cropped_image)
    except Exception as e:
        logging.error(f"Error at file {image_path} with description: {str(e)}")
    progress_bar.update(1)

progress_bar.close()
