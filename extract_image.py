import glob

from pdf2image import convert_from_path
from pdf2image.exceptions import (PDFInfoNotInstalledError, PDFPageCountError, PDFSyntaxError)
from tqdm import tqdm

# Get a list of all PDF files in the directory
pdf_files = glob.glob("downloaded_pdf/*.pdf")

# Set up tqdm to display a progress bar
progress_bar = tqdm(total=len(pdf_files), desc='Processing PDFs', unit='file')

# Loop through each PDF file
for pdf_file in pdf_files:
    try:
        # Convert PDF to images
        images = convert_from_path(pdf_file, output_folder='extract_images', fmt='jpeg', thread_count=2)

        # Update the progress bar
        progress_bar.update(1)

    except (PDFInfoNotInstalledError, PDFPageCountError, PDFSyntaxError) as e:
        print(f"Error processing {pdf_file}: {e}")

# Close the progress bar
progress_bar.close()