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

        if link and not link.startswith('http'):
            link = f"https://www.jumia.com.ng{link}"
        products.append({
            'description': description,
            'link': link,
            'image': image
        })

    return products

# Streamlit app
st.markdown(
    "<p style='color:coral;font-size:50px;font-family: verdana;'>Jumia Product Scraper</p>", 
    unsafe_allow_html=True
)
st.markdown(
    "<p style='color:red;'>Note: Due to other people's requests being made, it could lead to slower data fetching!</p>", 
    unsafe_allow_html=True
)
param = st.text_input("Enter the product to search:", "nokia")

# Scrape and display results on button click
st.markdown(
    """
    <style>
    .stButton > button {
        background-color: black;
        color: coral;
        font-size: 20px;
        font-family: Verdana, sans-serif;
        border: none;
        border-radius: 10px;
        padding: 10px 20px;
        cursor: pointer;
        transition: background-color 0.3s;
    }
    .stButton > button:hover {
        background-color: coral;
        color: black;
    }
    .rounded-img {
        border-radius: 15px;
    }
    .view-product-btn {
        display: inline-block;
        background-color: black;
        color: white;
        padding: 10px 20px;
        font-size: 18px;
        border-radius: 10px;
        text-decoration: none;
        transition: background-color 0.3s;
    }
    .view-product-btn:hover {
        background-color: coral;
        color: black;
    }
    .separator {
    border-top: 2px solid coral;
    margin: 10px 0;
}
    </style>
    """, 
    unsafe_allow_html=True
)
if st.button("Scrape Products"):
    st.write(f"Scraping products for: **{param}**...")

    products = scrape_jumia(param)

    if products:
        # Display the products
        for product in products:
            st.markdown('<hr class="separator">', unsafe_allow_html=True)
            st.text(product['description'])
            if product['image']:
                st.markdown(f"<img src='{product['image']}' class='rounded-img' width='250'>", unsafe_allow_html=True)
            st.markdown(f"<a href='{product['link']}' class='view-product-btn' target='_blank'>View Product</a>", unsafe_allow_html=True)
    else:
        st.warning("No products found.")
