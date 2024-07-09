import os
import cv2
import pytesseract
import numpy as np
import re

# Specify the path to the Tesseract executable
# This step is necessary for Windows users
#pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Directory containing the images
image_directory = 'images'

# Output file
output_file = 'output.txt'

# Get a list of all image files in the directory
image_files = [f for f in os.listdir(image_directory) if f.endswith(('.jpg', '.png'))]

# Sort the image files by creation time (oldest first)
image_files.sort(key=lambda x: os.path.getctime(os.path.join(image_directory, x)))

# Open the output file in write mode
with open(output_file, 'w') as f:
    # Loop through each file in the sorted list
    for filename in image_files:
        # Construct the full file path
        filepath = os.path.join(image_directory, filename)
        # Read the image using OpenCV
        img = cv2.imread(filepath)
        # Convert the image to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # Resize the image to enhance details
        gray = cv2.resize(gray, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
        # Apply thresholding to make the image binary
        _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        # Invert the image to ensure numbers are white on a black background
        inverted = cv2.bitwise_not(thresh)
        # Use pytesseract to extract text from the preprocessed image, focusing on digits
        custom_config = '--psm 6 digits'
        text = pytesseract.image_to_string(inverted, config=custom_config)
        # Extract only numbers from the text
        numbers = ''.join(re.findall(r'\d+', text))
        # Write the extracted numbers to the output file
        f.write(numbers + '\n')
        print(f"Processed image: {filename}; data: {numbers}")

print("Number extraction completed. Check the output file.")
