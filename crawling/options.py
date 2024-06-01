from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

##from webdriver_manager.chrome import ChromeDriverManager
##s = Service(executable_path=ChromeDriverManager().install())

opt = webdriver.ChromeOptions()
opt.add_argument("window-size=1700,2000")
opt.add_argument("no-sandox")
opt.add_argument('--headless')

##chrome = webdriver.Chrome("./chromedriver", service=s, options=opt)

##chrome.get("https://www.naver.com/")