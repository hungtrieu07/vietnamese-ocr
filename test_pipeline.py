from shutil import rmtree
import traceback
from PIL import Image
import fitz  # PyMuPDF
import os
from paddleocr import PaddleOCR
from sympy import use
from torch import device
from vietocr.tool.predictor import Predictor
from vietocr.tool.config import Cfg
import cv2
import numpy as np

def init_ocr_models():
    try:
        # Initialize PaddleOCR for detection
        paddle_ocr = PaddleOCR(use_angle_cls=True, lang='en', use_gpu=True)
        
        # Initialize VietOCR for recognition
        config = Cfg.load_config_from_name('vgg_transformer')
        config['device'] = 'cuda:0'  # Change to 'cuda' if using GPU
        config['cnn']['pretrained'] = True
        config['predictor']['beamsearch'] = True
        viet_ocr = Predictor(config)
        
        return paddle_ocr, viet_ocr
    except Exception as e:
        import traceback; traceback.print_exc();
        print(f"Error initializing OCR models: {e}")

def process_image_with_ocr(image_path, paddle_ocr, viet_ocr):
    try:
        # Read image
        image = cv2.imread(image_path)
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Detection using PaddleOCR
        result = paddle_ocr.ocr(image_path, rec=False)
        boxes = [line for line in result[0]]
        
        # Sort boxes by their y-coordinates (top-to-bottom)
        boxes = sorted(boxes, key=lambda box: (np.min(np.array(box)[:, 1]), np.min(np.array(box)[:, 0])))
        
        text_results = []
        # Recognition using VietOCR
        for box in boxes:
            try:
                # Get coordinates and crop image
                points = np.array(box).astype(np.int32)
                x_min, y_min = points.min(axis=0)
                x_max, y_max = points.max(axis=0)
                crop_img = image_rgb[y_min:y_max, x_min:x_max]
                
                # Convert to PIL Image for VietOCR
                crop_pil = Image.fromarray(crop_img)
                
                # Recognize text
                text = viet_ocr.predict(crop_pil)
                text_results.append((box, text))
            except Exception as e:
                print(f"Error processing box: {e}")
                continue
        
        return text_results
    except Exception as e:
        import traceback; traceback.print_exc();
        print(f"Error processing image with OCR: {e}")

def pdf_to_images_and_ocr(pdf_path, output_folder, zoom_x=2, zoom_y=2):
    try:
        # Create output folder if it doesn't exist
        rmtree(output_folder, ignore_errors=True)
        os.makedirs(output_folder, exist_ok=True)
        
        # Initialize OCR models
        paddle_ocr, viet_ocr = init_ocr_models()
        
        # Open the PDF file
        pdf_document = fitz.open(pdf_path)
        
        all_results = {}
        # Iterate through each page
        for page_num in range(len(pdf_document)):
            page = pdf_document.load_page(page_num)
            
            # Set higher resolution using zoom factors
            mat = fitz.Matrix(zoom_x, zoom_y)
            pix = page.get_pixmap(matrix=mat)
            
            # Save the image
            image_path = f"{output_folder}/page_{page_num + 1}.png"
            pix.save(image_path)
            print(f"Saved {image_path}")
            
            # Perform OCR
            text_results = process_image_with_ocr(image_path, paddle_ocr, viet_ocr)
            all_results[f"page_{page_num + 1}"] = text_results
            
            # Save OCR results
            with open(f"{output_folder}/page_{page_num + 1}_ocr.txt", 'w', encoding='utf-8') as f:
                for _, text in text_results:
                    f.write(f"{text}\n")
        return all_results
    except Exception as e:
        import traceback; traceback.print_exc();
        print(f"Error processing PDF to images and OCR: {e}")

if __name__ == "__main__":
    pdf_path = "test.pdf"
    output_folder = "output"
    results = pdf_to_images_and_ocr(pdf_path, output_folder, zoom_x=3, zoom_y=3)