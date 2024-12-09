import streamlit as st
import requests
from bs4 import BeautifulSoup

# ScraperAPI Key
SCRAPERAPI_KEY = "473441c00cfe587c257f687c5e604ca9"

# Function to scrape Jumia
def scrape_jumia(param):
    # ScraperAPI URL with parameters
    scraperapi_url = f"http://api.scraperapi.com/?api_key={SCRAPERAPI_KEY}&url=https://www.jumia.com.ng/catalog/?q={param}"
    
    response = requests.get(scraperapi_url)

    # Check if the response is valid
    if response.status_code == 403:
        st.error("Access Denied! ScraperAPI request failed.")
        return []
    elif response.status_code != 200:
        st.error(f"Failed to retrieve data. Status Code: {response.status_code}")
        return []

    # Parse the page using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')
    products = []

    # Select product elements
    product_elements = soup.select('a.core')

    # Extract product details
    for element in product_elements:
        description = element.get_text().strip()
        link = element.get('href')
        image = element.find('img')['data-src'] if element.find('img') else None

        products.append({
            'description': description,
            'link': link,
            'image': image
        })

    return products

# Streamlit app
st.title("Jumia Product Scraper (ScraperAPI)")

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
