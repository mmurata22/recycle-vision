import sys
import requests

def translate_to_english(text):
    translation_map = {
        "plastica": "plastic",
        "bottiglia": "bottle",
        "vetro": "glass",
        "metallo": "metal",
        "cartone": "cardboard",
        "es:green dot": "green dot",
        "plastica,bottiglia,es:green dot,bottiglia pet": "plastic bottle, green dot"
    }
    return translation_map.get(text.lower(), text)

def find_custom_instructions(packaging_text, packaging_tags):
    recycling_instructions_map = {
        "plastic bottle": "Check local guidelines for plastic types (e.g., PET, HDPE). Clean and dry before recycling.",
        "plastic": "Check local guidelines for plastic types. Clean and dry before recycling.",
        "bottle": "Rinse the bottle and check if the cap can be recycled with it. Place in the plastics or glass bin.",
        "glass": "Rinse clean and place in your designated glass recycling container. Labels can often be left on.",
        "metal": "Empty and rinse the can. Place in your metals recycling bin.",
        "cardboard": "Flatten the box and ensure it is clean and dry. Place in the paper/cardboard recycling bin.",
        "paper": "Ensure the paper is clean and dry. Check for plastic linings which may make it non-recyclable."
    }
    
    all_text = packaging_text.lower() + ' ' + ' '.join(packaging_tags).lower()

    if "plastic bottle" in all_text:
        return recycling_instructions_map["plastic bottle"]
    
    for keyword, instruction in recycling_instructions_map.items():
        if keyword in all_text:
            return instruction

    return "Specific instructions not available. Please check local regulations."

def get_product_packaging_info(ean_code):
    url = f"https://en.openfoodfacts.org/api/v0/product/{ean_code}.json"
    r = requests.get(url)
    data = r.json()

    if data.get("status") != 1:
        return None

    product = data["product"]
    packaging = product.get("packaging", "Unknown")
    packaging_tags = product.get("packaging_tags", [])
    
    def remove_prefix(tag):
        if ':' in tag:
            return tag.split(':', 1)[-1]
        return tag
    
    translated_packaging = translate_to_english(packaging)
    cleaned_packaging_tags = [remove_prefix(translate_to_english(tag)).lower() for tag in packaging_tags]
    
    recyclable = is_recyclable(cleaned_packaging_tags, translated_packaging)
    custom_instructions = find_custom_instructions(translated_packaging, cleaned_packaging_tags)

    return {
        "packaging": translated_packaging,
        "packaging_tags": cleaned_packaging_tags,
        "recyclable": recyclable,
        "recycling_instructions": product.get("recycling_instructions", "Not available"),
        "custom_instructions": custom_instructions
    }

def is_recyclable(packaging_tags, packaging_text):
    recyclable_keywords = [
        "plastic", "bottle", "glass", "metal", "cardboard", "paper", "recyclable", "riciclabile", 
        "recyclé", "recyc", "recykl", "recycle", "green dot",
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
        print(f"Custom Instructions: {info['custom_instructions']}")
    else:
        print("Product not found.")