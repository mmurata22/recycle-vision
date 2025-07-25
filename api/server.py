from flask import Flask, request, jsonify
from flask_cors import CORS
import tempfile
import os
import sys

# Import the functions from your other two scripts
from recycle_vision import scan_barcodes_from_image
from product_finder import get_product_packaging_info

# Create the Flask app and enable CORS
app = Flask(__name__)
CORS(app)

@app.route('/scan_barcode', methods=['POST'])
def scan_barcode():
    if 'image' not in request.files:
        return jsonify({"success": False, "error": "No image file provided"}), 400

    file = request.files['image']

    # Use a temporary file to save the uploaded image
    # This is safer than using a hardcoded path and handles cleanup automatically
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as temp_image:
            file.save(temp_image)
            temp_image_path = temp_image.name

        # Call the barcode scanning function from recycle_vision.py
        barcodes = scan_barcodes_from_image(temp_image_path)

        # Cleanup: delete the temporary image file
        os.remove(temp_image_path)

        if not barcodes:
            return jsonify({"success": False, "error": "No barcode found in image"}), 404

        # Get the first barcode from the list (assuming one barcode per image)
        barcode = barcodes[0]

        # Call the product finder function from product_finder.py
        product_info = get_product_packaging_info(barcode)

        if product_info:
            return jsonify({
                "success": True, 
                "barcode": barcode,
                "packaging": product_info['packaging'],
                "recyclable": product_info['recyclable'],
                "recycling_instructions": product_info['recycling_instructions']
            })
        else:
            return jsonify({"success": False, "error": "Product not found"}), 404

    except Exception as e:
        print(f"An error occurred: {e}", file=sys.stderr)
        return jsonify({"success": False, "error": f"Internal server error: {e}"}), 500

if __name__ == '__main__':
    # Run the Flask app on port 5000 in debug mode
    app.run(port=5000, debug=True)