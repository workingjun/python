from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import time

class ReviewManager():
    def __init__(self, driver):
        self.driver = driver
        self.location = "arguments[0].scrollIntoView({ behavior: 'auto', block: 'center', inline: 'center' });"
    
    def Loading_reviews(self, url, stars_num):
        self.driver.get(url)
        time.sleep(2)

        elem = self.driver.find_element(By.NAME, 'review')
        self.driver.execute_script(self.location, elem)
        elem.click()
        time.sleep(2)

        xpath = "//div[@class='sdp-review__article__order__star__all']"
        elem = self.driver.find_element(By.XPATH, xpath)
        elem.click()

        xpath = "//ul[@class='sdp-review__article__order__star__list']"
        elem = self.driver.find_element(By.XPATH, xpath)
        elems = elem.find_elements(By.TAG_NAME, 'li')
        elems[5-stars_num].click()
        
        raw = self.driver.page_source
        search = BeautifulSoup(raw, 'html.parser')

        box = search.find("section", {"class": "js_reviewArticleListContainer"})
        reviews = box.find_all("article")

        re_text = ''

        for review in reviews:
            re = review.text.split('\n')

            for i in range(len(re)):
                re[i] = re[i].strip()
            
            while '' in re:
                re.remove('')

            for i in range(4):
                re.pop()
                
            for re1 in re:
                re_text += re1 + '\n'

        return re_text