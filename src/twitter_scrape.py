from selenium import webdriver 
from selenium.webdriver.common.by import By 
from selenium.webdriver.chrome.service import Service 
from selenium.webdriver.chrome.options import Options 
from selenium.webdriver.common.action_chains import ActionChains 
from selenium.webdriver.common.keys import Keys 
import time 
import random 
import json 
 
 
def load_cookies(driver, cookies_file): 
    """ 
    Load cookies from a file and add them to the browser session. 
    """ 
    with open(cookies_file, 'r') as file: 
        cookies = json.load(file) 
    for cookie in cookies: 
        driver.add_cookie(cookie) 
 
 
def random_delay(min_delay=1, max_delay=3): 
    """ 
    Introduce a random delay to avoid detection. 
    """ 
    time.sleep(random.uniform(min_delay, max_delay)) 
 
 
def scrape_twitter(url, cookies_file): 
    """ 
    Scrapes a Twitter webpage using cookies for authentication. 
    """ 
    # Configure Selenium WebDriver 
    options = Options() 
    options.add_argument("--headless")  # Run in headless mode 
    options.add_argument("--disable-blink-features=AutomationControlled")  # Avoid detection 
    options.add_argument("start-maximized")  # Start browser maximized 
    options.add_argument(f"user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36") 
 
    # Path to your WebDriver 
    service = Service(executable_path='drivers/chromedriver.exe') 
    driver = webdriver.Chrome(service=service, options=options) 
 
    try: 
        # Open Twitter 
        driver.get("https://x.com/home") 
        random_delay(2, 5) 
 
        # Load cookies 
        load_cookies(driver, cookies_file) 
        driver.refresh()  # Refresh to apply cookies 
        random_delay(3, 7) 
 
        # Navigate to the desired Twitter URL 
        driver.get(url) 
        random_delay(3, 7) 
 
        # Find all elements with the specific class combinations for "What's new" section
        whats_new_elements = driver.find_elements(
            By.CSS_SELECTOR, 
            "div.css-146c3p1.r-bcqeeo.r-1ttztb7.r-qvutc0.r-37j5jr.r-a023e6.r-rjixqe.r-b88u0q.r-1bymd8e"
        )
        
        for idx, element in enumerate(whats_new_elements):
            try:
                # Try to find the text content within span elements
                spans = element.find_elements(By.CSS_SELECTOR, "span.css-1jxf684.r-bcqeeo.r-1ttztb7.r-qvutc0.r-poiln3")
                if spans:
                    for span in spans:
                        content = span.text
                        if content:  # Only print if content is not empty
                            print(f"Trending {idx + 1}: {content}")
                else:
                    # If no span found, try to get direct text
                    content = element.text
                    if content:
                        print(f"Trending {idx + 1}: {content}")
                        
            except Exception as e:
                print(f"Error parsing trending topic {idx + 1}: {e}")
        
        random_delay(1, 3)
 
    except Exception as e:
        print(f"An error occurred: {e}") 
 
    finally:
        driver.quit() 
 
 
if __name__ == "__main__": 
    # Replace with the path to your cookies file and desired Twitter URL 
    cookies_file_path = "cookies/twitter_cookies.json" 
    twitter_url = "https://x.com/home?lang=en" 
 
    scrape_twitter(twitter_url, cookies_file_path)