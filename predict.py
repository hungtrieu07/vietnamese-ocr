# PREDICT SINGLE ONE IMAGE

# import argparse
# import glob
# import os
# import sys

# import cv2
# import torch
# from PIL import Image
# from vietocr.tool.config import Cfg
# from vietocr.tool.predictor import Predictor


# def main():
#     parser = argparse.ArgumentParser(description="Example script with a required command line argument",
#                                      formatter_class=argparse.ArgumentDefaultsHelpFormatter)
#     parser.add_argument("-F", "--file", type=str, help="input file or folder path", required=True)
#     args = parser.parse_args()

#     # Check if the provided path is a file or a folder
#     if os.path.isfile(args.file):
#         img_paths = [args.file]
#     elif os.path.isdir(args.file):
#         img_paths = glob.glob(os.path.join(args.file, '*.jpg'))
#     else:
#         print("Error: The provided path is neither a file nor a folder.")
#         sys.exit(1)

#     # Open the annotation file for writing
#     with open("annotation.txt", "w", encoding="utf-8") as f:
#         # Configure VietOCR
#         config = Cfg.load_config_from_name('vgg_transformer')

#         if torch.cuda.is_available():
#             config['device'] = "cuda:0"
#         else:
#             config['device'] = "cpu"

#         config['cnn']['pretrained'] = True
#         config['trainer']['batch_size'] = 2048
#         print(config)

#         recognitor = Predictor(config)

#         # Process each image
#         for img_path in img_paths:
#             img = cv2.imread(img_path)
#             img = Image.fromarray(img)
#             rec_result = recognitor.predict(img)
#             f.write(os.path.basename(img_path) + "\t" + rec_result + "\n")
#             # print(img_path + "\t" + rec_result)

#     print("Processing completed. Results written to annotation.txt.")

# if __name__ == "__main__":
#     main()

# PREDICT BATCH OF IMAGES
import argparse
import glob
import os
import sys

import cv2
import torch
from PIL import Image
from vietocr.tool.config import Cfg
from vietocr.tool.predictor import Predictor


def main():
    parser = argparse.ArgumentParser(description="Example script with a required command line argument",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-F", "--file", type=str, help="input file or folder path", required=True)
    args = parser.parse_args()

    # Check if the provided path is a file or a folder
    if os.path.isfile(args.file):
        img_paths = [args.file]
    elif os.path.isdir(args.file):
        img_paths = glob.glob(os.path.join(args.file, '*.jpg'))
    else:
        print("Error: The provided path is neither a file nor a folder.")
        sys.exit(1)
        
    # Configure VietOCR
    config = Cfg.load_config_from_name('vgg_transformer')

    if torch.cuda.is_available():
        config['device'] = "cuda:0"
    else:
        config['device'] = "cpu"

    config['cnn']['pretrained'] = True
    config['trainer']['batch_size'] = 2048
    print(config)

    recognitor = Predictor(config)

    # Open the annotation file for writing
    with open("annotation.txt", "w", encoding="utf-8") as f:

        # Process images in batches
        batch_size = 16  # Adjust the batch size based on your available memory
        for i in range(0, len(img_paths), batch_size):
            batch_paths = img_paths[i:i + batch_size]
            batch_images = [cv2.imread(path) for path in batch_paths]
            batch_images = [Image.fromarray(img) for img in batch_images]

            # Use the predict_batch method to get predictions for the batch
            batch_results = recognitor.predict_batch(batch_images)

            # Write results to the annotation file
            for path, result in zip(batch_paths, batch_results):
                f.write(os.path.basename(path) + "\t" + result + "\n")

    print("Processing completed. Results written to annotation.txt.")


if __name__ == "__main__":
    main()
