import sys
import requests

def get_product_packaging_info(ean_code):
    url = f"https://world.openfoodfacts.org/api/v0/product/{ean_code}.json"
    r = requests.get(url)
    data = r.json()

    if data.get("status") != 1:
        return None

    product = data["product"]
    packaging = product.get("packaging", "Unknown")
    packaging_tags = product.get("packaging_tags", [])
    recycling_instructions = product.get("recycling_instructions", "Not available")

    recyclable = is_recyclable(packaging_tags, packaging)

    return {
        "packaging": packaging,
        "packaging_tags": packaging_tags,
        "recyclable": recyclable,
        "recycling_instructions": recycling_instructions,
    }

def is_recyclable(packaging_tags, packaging_text):
    recyclable_keywords = [
        "plastic", "bottle", "glass", "metal", "cardboard", "paper", "cartone", "vetro", "plastica", 
        "metallo", "bottiglia", "recyclable", "riciclabile", "recyclé", "recyc", "recykl", "recycle",
        "green dot",
    ]

    for tag in packaging_tags:
        tag_lower = tag.lower()
        if any(keyword in tag_lower for keyword in recyclable_keywords):
            return True

    packaging_text_lower = packaging_text.lower()
    if any(keyword in packaging_text_lower for keyword in recyclable_keywords):
        return True

    return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide a barcode number (EAN) as an argument.")
        sys.exit(1)

    ean = sys.argv[1]
    info = get_product_packaging_info(ean)

    if info:
        print(f"Packaging description: {info['packaging']}")
        print(f"Packaging tags: {info['packaging_tags']}")
        print(f"Recyclable? {'Yes' if info['recyclable'] else 'No'}")
        print(f"Recycling instructions: {info['recycling_instructions']}")
    else:
        print("Product not found.")
