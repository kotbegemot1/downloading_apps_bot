import time
import os

from dotenv import load_dotenv, find_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import Service
from selenium.webdriver.common.by import By

load_dotenv(find_dotenv())

def get_url_by_selenium(url):
    s = Service(executable_path=os.getenv("executable_path_chrome"))
    
    options = webdriver.ChromeOptions()
    options.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36")
    # options.add_argument("--no-sandbox")
    options.add_argument("--headless")

    # driver = webdriver.Chrome(executable_path=os.getenv(executable_path_chrome), options=options)
    driver = webdriver.Chrome(service=s, options=options)

    try:
        driver.get(url=url)
        time.sleep(2)
        # info = [driver.find_element_by_class_name("variant").get_attribute("href"), driver.find_element_by_class_name("variant").text]
        # return driver.find_element_by_class_name("variant").get_attribute("href")
        return driver.find_element(By.CLASS_NAME, "variant").get_attribute("href")

        # return driver.page_source
    except Exception as e:
        print(e)
    finally:
        driver.close()
        driver.quit()

def main():
    # pass
    print(get_url_by_selenium("https://apkcombo.com/ru/marketplace/com.marketplace.marketplace/download/apk"))

if __name__ == '__main__':
    main()
    