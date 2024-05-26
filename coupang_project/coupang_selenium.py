from selenium import webdriver
from selenium.webdriver.common.by import By
import chromedriver_autoinstaller
import subprocess
import time

class option_click():
    def __init__(self, driver):
        self.driver = driver
    
    def get_keyword(self, keyword):
        xpath='//*[@id="headerSearchKeyword"]'
        self.driver.find_element(By.XPATH, xpath).send_keys(keyword)
        self.driver.find_element(By.XPATH, xpath).send_keys("\n")
    
    def min_max_Price(self, minPrice, maxPrice):
        elems = self.find_options()
        index = self.load("가격")

        xpath = "//input[@title='minPrice']"
        elems[index].find_element(By.XPATH, xpath).send_keys(str(minPrice))

        xpath = "//input[@title='maxPrice']"
        elems[index].find_element(By.XPATH, xpath).send_keys(str(maxPrice))

        xpath = '//*[@id="searchPriceFilter"]/div/a'
        elems[index].find_element(By.XPATH, xpath).click()

    def spec(self, option_name, num_of_which_option):
        elems = self.find_options()
        index = self.load(option_name)

        elems_option1 = elems[index].find_elements(By.TAG_NAME, 'li')
        elems_option1[num_of_which_option].click()

    def find_options(self):
        xpath = "//div[contains(@class, 'search-filter-options search-')]"
        elems = self.driver.find_elements(By.XPATH, xpath)

        return elems
    
    def load(self, option_name):
        elems = self.find_options()

        for i, elem in enumerate(elems):
            textbox = elem.text
            words = textbox.split()
            if option_name in words:
                index = i

        try:
            elems[index].find_element(By.TAG_NAME, 'span').click()
        except:
            pass

        return index
    
    def load_print(self, option_name):
        elems = self.find_options()

        for i, elem in enumerate(elems):
            textbox = elem.text
            words = textbox.split()
            if option_name in words:
                index = i

        try:
            elems[index].find_element(By.TAG_NAME, 'span').click()
        except:
            pass
        
        for elem in elems:
            print(elem.text)

