import requests
from bs4 import BeautifulSoup

# Function to fetch and parse the product page
def scrape_product_details(product_url):
    try:
        # Fetch the page content
        response = requests.get(product_url)
        response.raise_for_status()  # Raise exception for HTTP errors
        
        # Parse the page content
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract product images
        image_tags = soup.find_all('img', class_='details-gallery__picture')
        images = [{'url': img['src']} for img in image_tags if 'src' in img.attrs]
        
        # Extract available sizes (if any)
        size_select = soup.find('select', {'aria-label': 'Size'})
        sizes = [option.text.strip() for option in size_select.find_all('option') if option.get('value')] if size_select else []
        
        # Extract available colors
        color_select = soup.find('select', {'aria-label': 'Color'})
        colors = [option.text.strip() for option in color_select.find_all('option') if option.get('value')] if color_select else []
        
        return {
            'images': images,
            'sizes': sizes,
            'colors': colors
        }
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the product page: {e}")
        return None

# Provide the product URL
product_url = "https://jhbbedding.company.site/GEOMETRIC-FLEECE-SHEET-SET-p629460701"


# Scrape the product details
product_details = scrape_product_details(product_url)

# Display the extracted details
if product_details:
    print("Product Images:")
    for idx, img in enumerate(product_details['images']):
        print(f"{idx + 1}. {img['url']}")

    print("\nAvailable Sizes:")
    print(", ".join(product_details['sizes']) if product_details['sizes'] else "No sizes available")

    print("\nAvailable Colors:")
    print(", ".join(product_details['colors']) if product_details['colors'] else "No colors available")





 