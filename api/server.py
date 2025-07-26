from flask import Flask, request, jsonify
from flask_cors import CORS
import tempfile
import os
import sys

from recycle_vision import scan_barcodes_from_image
from product_finder import get_product_packaging_info

app = Flask(__name__)
CORS(app)

@app.route('/scan_barcode', methods=['POST'])
def scan_barcode():
    if 'image' not in request.files:
        return jsonify({"success": False, "error": "No image file provided"}), 400

    file = request.files['image']

    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as temp_image:
            file.save(temp_image)
            temp_image_path = temp_image.name

        barcodes = scan_barcodes_from_image(temp_image_path)
        os.remove(temp_image_path)

        if not barcodes:
            return jsonify({"success": False, "error": "No barcode found in image"}), 404

        barcode = barcodes[0]
        
        product_info = get_product_packaging_info(barcode)

        if product_info:
            return jsonify({
                "success": True, 
                "barcode": barcode,
                "packaging": product_info.get('packaging'),
                "recyclable": product_info.get('recyclable'),
                "custom_instructions": product_info.get('custom_instructions'),
                "recycling_instructions": product_info.get('recycling_instructions')
            })
        else:
            return jsonify({"success": False, "error": "Product not found"}), 404

    except Exception as e:
        print(f"An error occurred: {e}", file=sys.stderr)
        return jsonify({"success": False, "error": f"Internal server error: {e}"}), 500

if __name__ == '__main__' and os.getenv("FLASK_ENV") != 'production':
    app.run(port=5000, debug=True)
