import undetected_chromedriver as uc 
from selenium.webdriver.remote.webdriver import By
from bs4 import BeautifulSoup
import re
import trafilatura
import pandas as pd
from tqdm import tqdm

class SeleniumCrawler:
    def __init__(self, headless = True):
        options = uc.ChromeOptions()
        if headless:
            options.add_argument('--headless')  # Run Chrome in headless mode
            options.add_argument('--blink-settings=imagesEnabled=false')  # Disable image loading
        self.driver = uc.Chrome(use_subprocess=True, options=options, version_main=113)
        if not headless: self.driver.set_window_size(800, 600)

    def crawl_href(self, url, regex_filter = "http"):
        prefix_list = url.split("/")[:-1]
        
        self.driver.get(url)
        page_source = self.driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        hrefs = []
        for a_tag in soup.find_all('a', href=True):
            href = a_tag.get('href')
            if re.match('^http[s]?://', href):
                hrefs.append(href)
            else:
                new_url = '/'.join(prefix_list) + href
                hrefs.append(new_url)

        filtered_hrefs = [link for link in hrefs if re.search(regex_filter, link)]
        return filtered_hrefs
    
    def crawl_meta(self, url):
        try:
            self.driver.get(url)
            page_source = self.driver.page_source
            html_content = trafilatura.extract(page_source)
        except Exception as e:
            print(f"*** Crawl Failed: {e}")
            page_source = None
            html_content = None
        return page_source, html_content
        
    def exit_driver(self):
        self.driver.quit()

    def get_href_by_css(self, url, css_selector = 'a[aria-label="Next Page"]'):
        try:
            self.driver.get(url)
            element = self.driver.find_element(By.CSS_SELECTOR, css_selector)
            return element.get_attribute('href')
        except:
            print("*** Element Not Found")
            return None

    def get_hrefs_by_css(self, url, css_selector = 'a[aria-label="Next Page"]'):
        try:
            self.driver.get(url)
            elements = self.driver.find_elements(By.CSS_SELECTOR, css_selector)
            return [element.get_attribute('href') for element in elements]
        except:
            print("*** Element Not Found")
            return None