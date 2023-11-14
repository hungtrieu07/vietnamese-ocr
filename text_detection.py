import glob
import os

import cv2
from paddleocr import PaddleOCR
from tqdm import tqdm

# Initialize PaddleOCR
ocr = PaddleOCR()

image_files = glob.glob("/home/hungtrieu07/Downloads/datasets/vietnamese_ocr/extract_images/*.jpg")

progress_bar = tqdm(total=len(image_files), desc='Processing images', unit='file')

for image_path in image_files:
    try:
        image_name = os.path.basename(image_path)
        img = cv2.imread(image_path)

        # Perform text detection
        result = ocr.ocr(img, det=True, rec=False, cls=False)
        result = result[:][:][0]

        # Create a directory to save cropped text images
        output_dir = 'cropped_text_images_2'
        os.makedirs(output_dir, exist_ok=True)

        # Create Boxes
        boxes = []
        for line in result:
            boxes.append([[int(line[0][0]), int(line[0][1])], [int(line[2][0]), int(line[2][1])]])

        boxes = boxes[::-1]

        EXPEND = 5
        for box in boxes:
            box[0][0] = box[0][0] - EXPEND
            box[0][1] = box[0][1] - EXPEND
            box[1][0] = box[1][0] + EXPEND
            box[1][1] = box[1][1] + EXPEND

        texts = []
        for box in boxes:
            cropped_image = img[box[0][1]:box[1][1], box[0][0]:box[1][0]]
            output_path = os.path.join(output_dir, f'cropped_text_{box[0][0]}_{box[0][1]}_{box[1][0]}_{box[1][1]}.png')
            cv2.imwrite(output_path, cropped_image)
            progress_bar.update(1)
    except Exception as e:
        print(str(e))
        pass

progress_bar.close()