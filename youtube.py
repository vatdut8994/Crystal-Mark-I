from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from webdata import driver
from pynput.keyboard import Key,Controller
import time

keyboard = Controller()
youtube_query = open('youtube query.txt', 'r')
query = youtube_query.read()
youtube_query.close()
driver.get("https://www.youtube.com/results?search_query="+query.replace(' ', '+'))
div = WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.CLASS_NAME, "ytd-item-section-renderer"))
)
lnks=driver.find_elements_by_tag_name("a")
for lnk in lnks:
    link = lnk.get_attribute('href')
    if 'watch?v' in str(link):
        driver.get(link)
        time.sleep(1)
        keyboard.press('k')
        keyboard.release('k') 
        break