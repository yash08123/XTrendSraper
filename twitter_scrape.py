from selenium import webdriver 
from selenium.webdriver.common.by import By 
from selenium.webdriver.chrome.service import Service 
from selenium.webdriver.chrome.options import Options 
from selenium.webdriver.common.action_chains import ActionChains 
from selenium.webdriver.common.keys import Keys 
import time 
import random 
import json 
from datetime import datetime
import os

def load_cookies(driver, cookies_file): 
    with open(cookies_file, 'r') as file: 
        cookies = json.load(file) 
    for cookie in cookies: 
        driver.add_cookie(cookie) 

def random_delay(min_delay=1, max_delay=3): 
    time.sleep(random.uniform(min_delay, max_delay)) 

def save_trends_to_file(trends, filename="twitter_trends.txt"):
    """
    Save trends to file with timestamp
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Create the content to write
    content = f"\n\n=== Trends captured at {timestamp} ===\n"
    for trend in trends:
        content += f"- {trend}\n"
    
    # Append to file if it exists, create if it doesn't
    mode = 'a' if os.path.exists(filename) else 'w'
    with open(filename, mode, encoding='utf-8') as f:
        f.write(content)
    
    return content

def scrape_twitter(url, cookies_file): 
    options = Options() 
    options.add_argument("--headless")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("start-maximized")
    options.add_argument(f"user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36") 

    service = Service(executable_path='drivers/chromedriver.exe') 
    driver = webdriver.Chrome(service=service, options=options) 
    
    trends_list = []

    try: 
        driver.get("https://x.com/home") 
        random_delay(2, 5) 

        load_cookies(driver, cookies_file) 
        driver.refresh()
        random_delay(3, 7) 

        driver.get(url) 
        random_delay(3, 7) 

        whats_new_elements = driver.find_elements(
            By.CSS_SELECTOR, 
            "div.css-146c3p1.r-bcqeeo.r-1ttztb7.r-qvutc0.r-37j5jr.r-a023e6.r-rjixqe.r-b88u0q.r-1bymd8e"
        )
        
        for idx, element in enumerate(whats_new_elements):
            try:
                spans = element.find_elements(By.CSS_SELECTOR, "span.css-1jxf684.r-bcqeeo.r-1ttztb7.r-qvutc0.r-poiln3")
                if spans:
                    for span in spans:
                        content = span.text
                        if content:
                            trends_list.append(content)
                else:
                    content = element.text
                    if content:
                        trends_list.append(content)
                        
            except Exception as e:
                print(f"Error parsing trending topic {idx + 1}: {e}")
        
        # Save trends to file and return the content
        saved_content = save_trends_to_file(trends_list)
        return trends_list

    except Exception as e:
        print(f"An error occurred: {e}") 
        return []

    finally:
        driver.quit() 

if __name__ == "__main__": 
    cookies_file_path = "cookies/twitter_cookies.json" 
    twitter_url = "https://x.com/home?lang=en" 
    scrape_twitter(twitter_url, cookies_file_path)