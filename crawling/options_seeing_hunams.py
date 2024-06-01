options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)
driver.get("https://kosis.kr/statHtml/statHtml.do?orgId=116&tblId=DT_MLTM_2082&conn_path=I2")