from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, InvalidArgumentException, WebDriverException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import os
import time




def dowmload_bg_images_from_urls(url:str, project:str, company:str, destination_folder:str) -> str: 
    """ 
    Try to download the images, store in a folder and return a new path where the database store
    it, else, this return the same input url.
    
    """
    # CREATE THE BOT WITH SELENIUM TO WRITE THE DATA SCRAPED IN THE FORM GOOGLE
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')

    # Setup ChromeDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    try:
        driver.get(url)
        time.sleep(2)
        img = driver.find_element(By.TAG_NAME, value="img")
        try:
            main_path = f"app/static/images/img-projects/{destination_folder}/{company}/"
            os.makedirs(main_path)
        except OSError:
            pass

        # for destination folder, is about if the dowmload background image or logo image
        with open(f'{main_path}{project}.png', 'wb') as file:
            file.write(img.screenshot_as_png)
        
        final_url = f'static/images/img-projects/{destination_folder}/{company}/{project}.png'
        
    except Exception:
        final_url = url
    
    driver.quit()
    
    return final_url