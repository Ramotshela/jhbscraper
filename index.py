import requests
from bs4 import BeautifulSoup
import csv
import time

# URL to main category mapping
main_category_mapping = {
    "TOWELS": "bathroom",
    "MATS": "bathroom",
    "STORAGE-&-ACCESSORIES": "homeware",
    "SHEETS": "bedroom",
    "KIDS-BEDDING": "bedroom",
    "SUPER-KING-COLLECTION": "bedroom",
    "QUILTS": "bedroom",
    "BEDDING-ESSENTIALS": "bedroom",
    "COMFORTERS": "bedroom",
    "DUVET-COVERS": "bedroom",
    "PILLOWS": "bedroom",
    "STORAGE": "homeware",
    "THROWS-FLEECE": "homeware",
    "BABY-BLANKETS": "homeware",
    "KING-SIZE-BLANKETS": "bedroom",
    "MINK-BLANKETS": "bedroom",
    "BOX-BLANKETS": "bedroom",
    "CARPETS": "homeware",
    "COUCH-COVERS": "homeware",
    "DECOR": "homeware",
    "CURTAINS-&-BLINDS": "homeware",
    "FURNITURE": "homeware",
    "APPLIANCES-GADGETS": "homeware",
    "HEATERS-FANS": "homeware",
    "BAKING": "kitchen",
    "COOKWARE": "kitchen",
    "GLASSWARE": "kitchen",
    "AIRFRYERS": "kitchen",
    "SERVEWARE": "kitchen",
    "APPLIANCES": "kitchen",
    "CUTLERY-UTENSILS-KNIFE-SETS": "kitchen",
    "KITCHEN-GADGETS-ESSENTIALS": "kitchen",
    "KETTLES": "kitchen",
    "DINNERWARE": "kitchen",
    "BREADBIN-CANISTER-SETS": "kitchen",
    "DRINKWARE": "kitchen"
}

# Function to determine the full category path
def get_full_category(url):
    # Extract the last part of the URL and remove extra formatting
    category_slug = url.split('/')[-1].split('-')[0].upper()
    # Get the main category using the mapping, default to "other"
    main_category = main_category_mapping.get(category_slug, "other")
    return f"{main_category} > {category_slug.lower()}"

# Function to handle requests with retries and exponential backoff
def get_with_retry(url, retries=5, backoff_factor=2):
    for attempt in range(retries):
        try:
            response = requests.get(url)
            if response.status_code == 429:  # Too Many Requests
                wait_time = backoff_factor ** attempt  # Exponential backoff
                print(f"Rate limit exceeded. Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
            else:
                response.raise_for_status()  # If status is not 429, raise error for other failed status codes
                return response
        except requests.exceptions.RequestException as e:
            print(f"Error fetching URL {url}: {e}")
            time.sleep(5)  # Wait before retrying on other errors
    print(f"Failed to fetch {url} after {retries} attempts.")
    return None  # Return None if all retries failed

# List of URLs to scrape
urls = [
    "https://jhbbedding.company.site/TOWELS-c149879256", 
"https://jhbbedding.company.site/MATS-c149879257", 
"https://jhbbedding.company.site/STORAGE-&-ACCESSORIES-c155410506", 
"https://jhbbedding.company.site/SHEETS-c149873004", 
"https://jhbbedding.company.site/KIDS-BEDDING-c149874754", 
"https://jhbbedding.company.site/SUPER-KING-COLLECTION-c149879252", 
"https://jhbbedding.company.site/QUILTS-c149879503", 
"https://jhbbedding.company.site/BEDDING-ESSENTIALS-c149882255", 
"https://jhbbedding.company.site/COMFORTERS-c149882501", 
"https://jhbbedding.company.site/DUVET-COVERS-c149882502", 
"https://jhbbedding.company.site/PILLOWS-c149987506", 
"https://jhbbedding.company.site/STORAGE-c163207253", 
"https://jhbbedding.company.site/THROWS-FLEECE-c149879258", 
"https://jhbbedding.company.site/BABY-BLANKETS-c149882257", 
"https://jhbbedding.company.site/KING-SIZE-BLANKETS-c149979758", 
"https://jhbbedding.company.site/MINK-BLANKETS-c149991005", 
"https://jhbbedding.company.site/BOX-BLANKETS-c165489159", 
"https://jhbbedding.company.site/CARPETS-c150143504", 
"https://jhbbedding.company.site/COUCH-COVERS-c150143754", 
"https://jhbbedding.company.site/STORAGE-c150156752", 
"https://jhbbedding.company.site/DECOR-c150169751", 
"https://jhbbedding.company.site/CURTAINS-&-BLINDS-c150170001", 
"https://jhbbedding.company.site/FURNITURE-c163209005", 
"https://jhbbedding.company.site/APPLIANCES-GADGETS-c163211004", 
"https://jhbbedding.company.site/HEATERS-FANS-c168595270", 
"https://jhbbedding.company.site/BAKING-c149874756", 
"https://jhbbedding.company.site/COOKWARE-c149879253", 
"https://jhbbedding.company.site/GLASSWARE-c149879254", 
"https://jhbbedding.company.site/STORAGE-c149879255", 
"https://jhbbedding.company.site/AIRFRYERS-c149879504", 
"https://jhbbedding.company.site/SERVEWARE-c149879505", 
"https://jhbbedding.company.site/APPLIANCES-c149882503", 
"https://jhbbedding.company.site/CUTLERY-UTENSILS-KNIFE-SETS-c149882504", 
"https://jhbbedding.company.site/KITCHEN-GADGETS-ESSENTIALS-c157177528", 
"https://jhbbedding.company.site/KETTLES-c158426062", 
"https://jhbbedding.company.site/DINNERWARE-c158434564", 
"https://jhbbedding.company.site/BREADBIN-CANISTER-SETS-c160457093", 
"https://jhbbedding.company.site/DRINKWARE-c163972663"

]

# Open the CSV file to write the product data
with open('products.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    # Write the header row
    writer.writerow([
        'Category', 'Product Name', 'Product ID', 'Product URL', 'Original Price', 
        'Price x 1.45', 'Price x 1.45 + 10%', 'Image URL'
    ])

    # Loop through each URL
    for url in urls:
        # Determine the full category
        category = get_full_category(url)

        # Fetch the page content with retry logic
        response = get_with_retry(url)
        if response is None:
            continue  # Skip to the next URL if the request failed after retries

        # Parse the page content with BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all product items
        products = soup.find_all('div', class_='grid-product__wrap-inner')

        # Loop through each product and extract relevant details
        for product in products:
            try:
                # Extract the product link (URL)
                product_url = product.find('a', class_='grid-product__image')['href']

                # Extract the product name (title)
                product_name = product.find('div', class_='grid-product__title-inner').get_text(strip=True)

                # Extract the product price (remove 'R' and commas, convert to float, and round to whole number)
                product_price_text = product.find('div', class_='grid-product__price-value').get_text(strip=True)
                product_price = round(float(product_price_text.replace('R', '').replace(',', '').strip()))

                # Calculate Price x 1.45 (rounded to whole number)
                price_x_1_45 = round(product_price * 1.45)

                # Calculate Price x 1.45 + 10% (rounded to whole number)
                price_x_1_45_plus_10 = round(price_x_1_45 * 1.10)

                # Extract the image URL
                image_url = product.find('img', class_='grid-product__picture')['src']

                # Extract the product ID (from data-product-id attribute)
                product_id = product.find('a', class_='grid-product__image')['data-product-id']

                # Write the product details to the CSV
                writer.writerow([
                    category, product_name, product_id, product_url, product_price, 
                    price_x_1_45, price_x_1_45_plus_10, image_url
                ])

                # Optionally print the product details for confirmation
                print(f"Category: {category}")
                print(f"Product Name: {product_name}")
                print(f"Product ID: {product_id}")
                print(f"Product URL: {product_url}")
                print(f"Original Price: {product_price}")
                print(f"Price x 1.45: {price_x_1_45}")
                print(f"Price x 1.45 + 10%: {price_x_1_45_plus_10}")
                print(f"Image URL: {image_url}")
                print('-' * 50)

                # Delay between requests to avoid too many requests error
                time.sleep(2)

            except Exception as e:
                print(f"Error processing product: {e}")

print("Product details have been written to 'products.csv'")
