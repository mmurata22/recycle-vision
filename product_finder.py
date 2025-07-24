import sys
import requests

def get_product_info(ean_code):
    url = f"https://world.openfoodfacts.org/api/v0/product/{ean_code}.json"
    response = requests.get(url)
    data = response.json()

    if data.get("status") == 1:
        product = data["product"]
        name = product.get("product_name", "Unknown")
        brand = product.get("brands", "Unknown")
        quantity = product.get("quantity", "Unknown")
        return {
            "name": name,
            "brand": brand,
            "quantity": quantity
        }
    else:
        return None

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide a barcode as argument")
        sys.exit(1)

    ean = sys.argv[1]
    info = get_product_info(ean)
    if info:
        print(f"Product name: {info['name']}")
        print(f"Brand: {info['brand']}")
        print(f"Quantity: {info['quantity']}")
    else:
        print("Product not found.")
