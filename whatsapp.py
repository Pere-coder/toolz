from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def send_whatsapp_message(phone_number, message, driver):
    try:
        url = f"https://web.whatsapp.com/send?phone={+2349011833652}&text={message}"
        driver.get(url)
        
        time.sleep(10) 
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//span[@data-icon="send"]'))
        )

        # Click the send button
        send_button = driver.find_element(By.XPATH, '//span[@data-icon="send"]')
        send_button.click()
        print(f"Message sent successfully to {phone_number}")

    except Exception as e:
        print(f"Failed to send message to {phone_number}: {e}")
        time.sleep(5)
        print(f"Message sent to {phone_number}")
    except Exception as e:
        print(f"Failed to send message to {phone_number}: {e}")

# Main script
if __name__ == "__main__":
    # Path to your ChromeDriver
    
    driver_path = "C:\\Users\\pere\\Downloads\\chromedriver-win64\\chromedriver-win64\\chromedriver.exe" 
    
    # Initialize ChromeOptions
    options = Options()
    options.binary_location = "C:\\Users\\pere\\Downloads\\chrome-win64\\chrome-win64\\chrome.exe"
    
    # Use Service to manage ChromeDriver
    service = Service(driver_path)
    
    # Initialize WebDriver with ChromeOptions
    driver = webdriver.Chrome(service=service, options=options)

    # Open WhatsApp Web
    driver.get("https://web.whatsapp.com")
    print("Scan the QR code to log in.")
    time.sleep(20) 
    
    phone_numbers = ["+2349157444437"]
    message = "Hello! This is an automated message."
    
    for number in phone_numbers:
        send_whatsapp_message(number, message, driver)
    
    # Close the browser
    driver.quit()
