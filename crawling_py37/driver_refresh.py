# 라이브러리 임포트
from selenium import webdriver

# 드라이버 실행 및 페이지 이동
driver = webdriver.Chrome()
url = "https://www.naver.com/"
driver.get(url)
driver.implicitly_wait(10)

# refresh method
driver.refresh()