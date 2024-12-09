import requests
from bs4 import BeautifulSoup
import re
import streamlit as st

# Scraping function using BeautifulSoup
def scrape_jumia(param):
    url = f"https://www.jumia.com.ng/catalog/?q={param}"  # Construct URL
    products = []

    try:
        # Send HTTP GET request to the URL
        response = requests.get(url)
        response.raise_for_status()  # Check for request errors (e.g., 404, 500)

        # Parse HTML using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Locate product elements (You may need to inspect the page to get the correct CSS selector)
        product_elements = soup.select('a.core')

        # Extract product details
        for element in product_elements:
            product_info = {}

            # Extract and clean text
            text = element.get_text()
            parts = re.split(r'\(\d+\)', text)  # Remove any numbers inside parentheses (e.g., price counts)
            parts = [part.strip() for part in parts if part.strip()]
            combined_text = " ".join(parts)

            # Extract link
            link = element.get('href')

            # Extract image
            image_element = element.find('img')
            if image_element:
                image_src = image_element.get('data-src') or image_element.get('src')
            else:
                image_src = None

            # Add to products list
            products.append({
                'description': combined_text,
                'link': link,
                'image': image_src
            })

    except Exception as e:
        st.error(f"An error occurred during scraping: {e}")

    return products

# Streamlit app
st.title("Jumia Product Scraper")

# Input field for product search
param = st.text_input("Enter the product to search:", "nokia")

# Scrape and display results on button click
if st.button("Scrape Products"):
    st.write(f"Scraping products for: **{param}**...")
    products = scrape_jumia(param)

    if products:
        # Display the products
        for product in products:
            st.subheader(product['description'])
            if product['image']:
                st.image(product['image'], width=150)
            st.markdown(f"[View Product]({product['link']})")
    else:
        st.warning("No products found.")

