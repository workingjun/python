from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.alert import Alert 
import time



def login(browser):
    browser.get('https://everytime.kr/')
    browser.maximize_window()

    ##/html/body/div/main/header/button
    elem = browser.find_element(By.XPATH, '/html/body/div/main/header/button')
    elem.click()

    elem = browser.find_element(By.XPATH, '/html/body/div/aside/div[2]/div[1]/a[1]')
    elem.click()

    elem = browser.find_element(By.XPATH, '/html/body/div[1]/div/form/div[1]/input[1]')
    elem.click()
    elem.send_keys("kim0102483")

    elem = browser.find_element(By.XPATH, '/html/body/div[1]/div/form/div[1]/input[2]')
    elem.click()
    elem.send_keys("junhee2483")

    elem.send_keys(Keys.ENTER)

    ##/html/body/div[1]/div/form/div[1]/input[1]
    ##/html/body/div[1]/div/form/div[1]/input[2]

    time.sleep(2)


def scroll_down(driver, Y):
    driver.execute_script(f"window.scrollTo(0, {Y})") 
    time.sleep(3)


def up_click(browser):
    num = 1.5
    
    for i in range(20):
        try:
            elem = browser.find_elements(By.CLASS_NAME, "list")

            time.sleep(1)
            elem2 = elem[i].find_element(By.CLASS_NAME, "article")
            elem2.click()

            scroll_down(browser, 300)

            elem3 = browser.find_element(By.CLASS_NAME, "posvote")
            elem3.click()

            time.sleep(2)
        except:
            pass

        else:
            try:
                alert = Alert(browser)
                time.sleep(1)
                
                alert.accept() # to click 'OK'
                time.sleep(1)

                alert.accept() # to click 'OK'
                time.sleep(1)

                browser.back()
                time.sleep(1)

            except:
                browser.back()
                time.sleep(1)

            else:
                num += 0.5
                scroll_down(browser, 210*num)