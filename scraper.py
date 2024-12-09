import streamlit as st
import requests
from bs4 import BeautifulSoup

def scrape_jumia(param):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    url = f"https://www.jumia.com.ng/catalog/?q={param}"
    response = requests.get(url, headers=headers)

    if response.status_code == 403:
        st.error("Access Denied! The server rejected your request.")
        return []

    # Parse the page using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')
    products = []

    product_elements = soup.select('a.core')

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
