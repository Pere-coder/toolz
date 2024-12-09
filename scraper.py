import re
import streamlit as st
from playwright.sync_api import sync_playwright
import time

# Scraping function using Playwright
def scrape_jumia(param):
    products = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Ensure headless mode
        page = browser.new_page()
        page.goto(f"https://www.jumia.com.ng/catalog/?q={param}")

        # Wait for page content to load
        page.wait_for_selector('a.core')

        # Extract product details
        product_elements = page.query_selector_all('a.core')
        for element in product_elements:
            description = element.inner_text()
            link = element.get_attribute('href')
            image = element.query_selector('img').get_attribute('data-src')

            products.append({
                'description': description,
                'link': link,
                'image': image
            })

        browser.close()

    return products

# Streamlit app
st.title("Jumia Product Scraper")

# Input field for product search
param = st.text_input("Enter the product to search:", "nokia")

# Scrape and display results on button click
if st.button("Scrape Products"):
    st.write(f"Scraping products for: **{param}**...")

    with st.spinner('Scraping products...'):
        time.sleep(2)  # Simulate waiting time for scraping
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
