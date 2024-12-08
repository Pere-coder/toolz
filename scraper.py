import re
import streamlit as st
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException


# Configure the ChromeDriver and browser binary paths
driver_path = "C:\\Users\\pere\\Downloads\\chromedriver-win64\\chromedriver-win64\\chromedriver.exe"
chrome_binary_path = "C:\\Users\\pere\\Downloads\\chrome-win64\\chrome-win64\\chrome.exe"

# Configure WebDriver with Chrome options
def configure_driver():
    options = Options()
    options.binary_location = chrome_binary_path
    service = Service(driver_path)
    return webdriver.Chrome(service=service, options=options)

# Scraping function
def scrape_jumia(param):
    driver = configure_driver()  # Initialize WebDriver
    url = f"https://www.jumia.com.ng/catalog/?q={param}"  # Construct URL
    products = []

    try:
        driver.get(url)
        driver.implicitly_wait(10)  # Wait for the page to load

        # Locate product elements
        product_elements = driver.find_elements(By.CSS_SELECTOR, 'a.core')

        # Extract product details
        for element in product_elements:
            product_info = {}

            # Extract and clean text
            text = element.text
            parts = re.split(r'\(\d+\)', text)
            parts = [part.strip() for part in parts if part.strip()]
            combined_text = " ".join(parts)

            # Extract link and image
            link = element.get_attribute('href')
            try:
                image_element = element.find_element(By.TAG_NAME, 'img')
                image_src = image_element.get_attribute('data-src') or image_element.get_attribute('src')
            except NoSuchElementException:
                image_src = None

            # Add to products list
            products.append({
                'description': combined_text,
                'link': link,
                'image': image_src
            })

    except Exception as e:
        st.error(f"An error occurred during scraping: {e}")
    finally:
        driver.quit()  # Close the browser

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
