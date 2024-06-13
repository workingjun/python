import requests
from bs4 import BeautifulSoup
from Class_2_Searching_coupang import CoupangManager as CM
import re

class ShopManager():       
        def __init__(self, driver):
                self.driver = driver

        def move_page(self, page_num):
                url = self.driver.current_url

                if re.search(r'page=\d+', url):
                        new_url = re.sub(r'page=\d+', f'page={page_num}', url)
                else:
                        new_url = f'{url}&page={page_num}'
                self.driver.get(new_url)
               
                raw = self.driver.page_source

                search = BeautifulSoup(raw, 'html.parser')
                return search
                
        def find_html(self, page_num):
                product_num = 1

                link_list, imageLink_list, title_list, price_list, point_list=[], [], [], [], [] 
                
                search = self.move_page(page_num)

                box = search.find('ul', {'id' : 'productList'})
                all_product = box.find_all('li', {'class': 'search-product'})

                for i, product in enumerate(all_product):
                        imagefind = product.find("img", {'class' : 'search-product-wrap-img'})
                        if imagefind.get("data-img-src") is None:
                                imageLink = "http:" + imagefind.get('src')
                        else:
                                imageLink = "http:" + imagefind.get("data-img-src")

                        title = product.find('div', {'class' : 'name'})
                        price = product.find('strong', {'class' : 'price-value'})
                        point = product.find('span', {'class' : 'rating-total-count'})

                        link2 = product.find('a')['href']
                        link = "https://www.coupang.com" + link2

                        imageLink_list.append(imageLink)
                        
                        title_text = f"{product_num}. {title.text.strip()}"

                        title_list.append(title_text)

                        if price is None:
                                price_list.append('')
                        else:
                                price_list.append(price.text)
                        

                        if point is None:
                                point_list.append('')
                        else:
                                point_list.append(point.text)
                        
                        link_list.append(link)    

                        product_num += 1

                return link_list, imageLink_list, title_list, price_list, point_list
