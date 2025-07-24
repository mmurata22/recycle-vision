from pyzbar import pyzbar
import cv2

def scan_barcodes_from_image(image_path):
    image = cv2.imread(image_path)
    if image is None:
        print("Failed to load image")
        return []

    barcodes = pyzbar.decode(image)
    barcode_data_list = []

    for barcode in barcodes:
        barcode_data = barcode.data.decode('utf-8')
        barcode_type = barcode.type
        print(f"Detected {barcode_type}: {barcode_data}")
        barcode_data_list.append(barcode_data)

    return barcode_data_list

if __name__ == "__main__":
    image_path = 'test_images/coca_cola_barcode.png'
    codes = scan_barcodes_from_image(image_path)
    print("Barcodes found:", codes)
