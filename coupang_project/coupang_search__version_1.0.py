import requests
from bs4 import BeautifulSoup

class Search():
    def __init__(self, keyword):
        self.link_list=[]
        self.imageLink_list=[]
        self.title_list=[]
        self.price_list=[]
        self.point_list=[]
        self.keyword =keyword  

    def elem_search(self):
        search_query = self.keyword
        page_num = 1

        while page_num<2:
            coupang_url = 'https://www.coupang.com/np/search?q='+ search_query + '&channel=user&component=&eventCategory=SRP&trcid=&traid=&sorter=scoreDesc&minPrice=&maxPrice=&priceRange=&filterType=&listSize=36&filter=&isPriceRange=false&brand=&offerCondition=&rating=0&page='+ str(page_num)+'&rocketAll=false&searchIndexingToken=1=9&backgroundColor='

            header={'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36", 
            "Accept-Language": "ko-KR,ko;q=0.9"}

            raw = requests.get(coupang_url, headers=header) 
            search = BeautifulSoup(raw.text, 'html.parser')

            box = search.find('ul', {'id' : 'productList'})
            all_product = box.find_all('li', {'class': 'search-product'})

            for product in all_product:
                # if i==0:
                #     continue
                try:
                    imagefind = product.find("dt", {'class' : 'image'})
                    imageLink = "http:" + imagefind.find("img", {'class' : 'search-product-wrap-img'})['src']

                    if "img1a" in imageLink:
                                    continue 
                    
                    title = product.find('div', {'class' : 'name'})
                    price = product.find('strong', {'class' : 'price-value'})
                    point = product.find('div', {'class' : 'other-info'}).find('span', {'class' : 'rating-total-count'})
                    link2 = product.find('a')['href']
                    link = "https://www.coupang.com" + link2

                    self.imageLink_list.append(imageLink)
                    self.title_list.append(title.text.strip())
                    self.price_list.append(price.text)
                    self.point_list.append(point.text)
                    self.link_list.append(link)
                except:
                    pass
                
            page_num+=1