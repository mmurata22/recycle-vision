import cv2
import pytesseract
from PIL import Image
import numpy as np
import sys

def preprocess_image(image_path):
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError("Image not found or cannot be opened")
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return thresh

def extract_text(image_path):
    processed_img = preprocess_image(image_path)
    pil_img - Image.fromarray(processed_img)
    return pytesseract.image_to_string(pil_img)

def determine_recyclability(text):
    text = text.lower()
    rules = {
        "pet": "Recyclable (Plastic #1 - PET)",
        "hdpe": "Recyclable (Plastic #2 = HDPE)",
        "pp": "Recyclable (Plastic #5 = PP)",
        "glass": "Recyclable (Glass)",
        "aluminum": "Recyclable (Aluminum)",
        "ps": "Not recyclable (Plastic #6 - Polysterene)",
        "non-recyclable": "Not recyclable",
        "other": "Not recyclable (Plastic #7 - Other)"      
    }

    for keyword, message in rules.items():
        if keyword in text:
            return message
    return "Unable to determine recyclability"

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python recycle_vision.py /path/to/image.jpg")
        sys.exit(1)
    
    image_path = sys.argv[1]
    try:
        text = extract_text(image_path)
        result = determine_recyclability(text)
        print("\n Extracted text:\n", text)
        print("\n Recyclability Verdict:\n", result)
    except Exception as e:
        print("Error:", e)