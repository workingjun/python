from selenium.webdriver.common.by import By
import time

class CoupangManager:
    def __init__(self, driver):
        self.driver = driver
        self.location = "arguments[0].scrollIntoView({ behavior: 'auto', block: 'center', inline: 'center' });"
        
    def Loading_Options(self):
        xpath = "//div[contains(@class, 'search-filter-options search-')]"
        elems = self.driver.find_elements(By.XPATH, xpath)

        return elems

    def page_source(self):
        return self.driver.page_source
    
###############################################################################################################

class Setting_Options(CoupangManager):
    def getting_keyword(self, keyword):
        elem = self.driver.find_element(By.ID, 'headerSearchKeyword')
        elem.send_keys(keyword)
        elem.send_keys("\n")

    def Click_option(self, option_name = None, option_item_name = None):
        elems = self.Loading_Options()

        if option_item_name is None:
            if option_name is None:
                for i in range(4, len(elems)-2):
                    try:
                        self.driver.execute_script(self.location, elems[i])
                        elems[i].find_element(By.TAG_NAME, 'span').click()

                    except:
                        continue
            else:
                option_num, _ = self.find_index_of_Options(option_name)
                self.driver.execute_script(self.location, elems[option_num])
                elems[option_num].find_element(By.TAG_NAME, 'span').click()
        else:
            option_num, _ = self.find_index_of_Options(option_name)

            try:
                more_view_elem = elems[option_num].find_element(By.TAG_NAME, 'span')
                if more_view_elem.get_attribute("style") != 'opacity: 1;':
                    self.driver.execute_script(self.location, elems[option_num])
                    more_view_elem.click()
            except:
                pass
            
            finally:
                option_num, option_item_num = self.find_index_of_Options(option_name, option_item_name)

                elems_option1 = elems[option_num].find_elements(By.TAG_NAME, 'li')
                self.driver.execute_script(self.location, elems_option1[option_item_num])
                elems_option1[option_item_num].click()    
                    
    def setting_Price(self, minPrice, maxPrice):
        elems = self.Loading_Options()
        index, _ = self.find_index_of_Options("가격")

        xpath = "//input[@title='minPrice']"
        elems[index].find_element(By.XPATH, xpath).send_keys(str(minPrice))

        xpath = "//input[@title='maxPrice']"
        elems[index].find_element(By.XPATH, xpath).send_keys(str(maxPrice))

        xpath = '//*[@id="searchPriceFilter"]/div/a'
        elems[index].find_element(By.XPATH, xpath).click()

    def print_Option_names(self):
        list1=[]

        text_list = self.Save_Options()
        
        for text in text_list:
            list1.append(text[0])
        
        return list1
    
    def print_Option_items(self, option_name):
        list1 = []

        option_num, _ = self.find_index_of_Options(option_name)
        text_list = self.Save_Options()
        
        for text in text_list[option_num - 4]:
            if text == option_name:
                continue
            else:
                list1.append(text)

        return list1

    def Save_Options(self):
        elems = self.Loading_Options()
        texts = [elem.text.split('\n') for elem in elems[4:]]
        text_list = []

        for i, text in enumerate(texts, start = 4):
            if text[-1] in ["닫기", "더보기"]:
                text.pop()
            if text[-1] == "검색":
                text.pop()
            if text[-1].endswith("~ 원"):
                text.pop()
            
            text_list.append(text)

        return text_list

    def find_index_of_Options(self, option_name, option_item_name = None):
        text_list = self.Save_Options()

        option_num = None
        option_item_num = None

        for i in range(len(text_list)):
            if text_list[i][0]==option_name:
                option_num = i + 4
                for j in range(len(text_list[i])):        
                    if text_list[i][j]==option_item_name:
                        option_item_num = j - 1
                        break
                if option_item_num is not None:
                    break

        return option_num, option_item_num  