import chromedriver_autoinstaller
import streamlit as st
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

# Automatically install the correct version of ChromeDriver
chromedriver_autoinstaller.install()

# Configure Chrome options for headless browsing


# Configure WebDriver for deployment
def configure_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    return webdriver.Chrome(options=options)

# Scraping function
def scrape_jumia(param):
    driver = configure_driver()
    url = f"https://www.jumia.com.ng/catalog/?q={param}"
    products = []

    try:
        driver.get(url)
        driver.implicitly_wait(10)

        # Locate product elements
        product_elements = driver.find_elements(By.CSS_SELECTOR, 'a.core')

        for element in product_elements:
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

            # Append to products list
            products.append({
                'description': combined_text,
                'link': link,
                'image': image_src
            })

    except Exception as e:
        st.error(f"An error occurred: {e}")
    finally:
        driver.quit()

    return products


# Streamlit app
st.title("Jumia Product Scraper")
param = st.text_input("Enter the product to search:", "nokia")

if st.button("Scrape Products"):
    st.write(f"Scraping products for: **{param}**...")
    products = scrape_jumia(param)

    if products:
        for product in products:
            st.subheader(product['description'])
            if product['image']:
                st.image(product['image'], width=150)
            st.markdown(f"[View Product]({product['link']})")
    else:
        st.warning("No products found.")
