import requests
from bs4 import BeautifulSoup

def scrape_product_page(url):
    # Make a request to the webpage
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to retrieve the page: {response.status_code}")
        return

    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract product name
    name = soup.find('h1', class_='product-details__product-title')
    name = name.text.strip() if name else 'N/A'

    # Extract product ID
    product_id = soup.find('meta', itemprop='sku')
    product_id = product_id['content'] if product_id else 'N/A'

    # Extract product description
    description = soup.find('meta', itemprop='description')
    description = description['content'] if description else 'N/A'

    # Extract images from `meta` tags and `product-gallery` class
    images = set()  # Use a set to avoid duplicates

    # From meta tags
    image_meta_tags = soup.find_all('meta', itemprop='image')
    for img_tag in image_meta_tags:
        images.add(img_tag['content'])

    # From product-gallery class
    gallery_images = soup.find('div', class_='product-gallery')
    if gallery_images:
        img_tags = gallery_images.find_all('a')
        for img in img_tags:
            if 'src' in img.attrs:
                images.add(img['src'])

    # Convert set back to list for JSON compatibility
    images = list(images)

    # Extract product options
    options = {}
    option_sections = soup.find_all('div', class_='product-details-module details-product-option')
    for section in option_sections:
        option_title = section.find('div', class_='product-details-module__title')
        if option_title:
            option_name = option_title.text.strip()
            option_values = [
                option['label']
                for option in section.find_all('option', label=True)
            ]
            options[option_name] = option_values

    # Compile product details
    product_details = {
        'Name': name,
        'Product ID': product_id,
        'Description': description,
        'Images': images,
        'Options': options
    }

    return product_details

# Example usage
url = "https://jhbbedding.company.site/KITCHEN-COMBO-p491523969"  # Replace with the product page URL
product_details = scrape_product_page(url)

if product_details:
    print("Product Details:")
    print(product_details)
