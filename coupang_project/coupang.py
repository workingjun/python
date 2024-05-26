from tkinter import *
from PIL import Image, ImageTk
from urllib.request import urlopen
from io import BytesIO
import requests
from bs4 import BeautifulSoup

index_num = 0
product_num = 1

def delete_and_insert():
    global imageLink_list, title_list, price_list, point_list, link_list

    display1.delete(1.0, END)
    display2.delete(1.0, END)
    display3.delete(1.0, END)
    display4.delete(1.0, END)

    display1.insert(1.0, title_list[index_num])
    display2.insert(1.0, price_list[index_num])
    display3.insert(1.0, point_list[index_num])
    display4.insert(1.0, link_list[index_num])

def img_insert():
    global link_list

    image_url = imageLink_list[index_num]

    with urlopen(image_url) as response:
        image_data = response.read()

        image = Image.open(BytesIO(image_data))
        photo = ImageTk.PhotoImage(image)

    label1.configure(image=photo)
    label1.image=photo

def keyword_submit():
    keyword_got = keyword_entry.get()
    keyword_got = f"<{keyword_got}의 쇼핑 목록>"
    information_list.configure(text=keyword_got)
    
def command_current():
    global index_num

    index_num=0

    img_insert()
    delete_and_insert()

def clickNext():
    global index_num, imageLink_list
        
    index_num+=1
    if index_num>len(imageLink_list)-1:
        index_num=0

    img_insert()
    delete_and_insert()

    
def clickPrev():
    global index_num, imageLink_list

    index_num-=1
    if index_num<0:
        index_num = len(imageLink_list)-1

    img_insert()
    delete_and_insert()

def search_action():
    global imageLink_list, title_list, price_list, point_list, link_list, product_num

    link_list = []
    imageLink_list = []
    title_list = []
    price_list = []
    point_list = []

    search_query = keyword_entry.get()
    page_num = int(page_num_entry.get())
    
    coupang_url = (
                f"https://www.coupang.com/np/search?q={search_query}"
                f"&channel=user&component=&eventCategory=SRP&trcid=&traid="
                f"&sorter=scoreDesc&minPrice=&maxPrice=&priceRange=&filterType="
                f"&listSize=36&filter=&isPriceRange=false&brand=&offerCondition=&rating=0&page="
                f"{page_num}&rocketAll=false&searchIndexingToken=1=9&backgroundColor="
                )
    header={
            'User-Agent': (
                        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) " 
                        "AppleWebKit/537.36 (KHTML, like Gecko) " 
                        "Chrome/121.0.0.0 Safari/537.36"
                        ), 
            "Accept-Language": "ko-KR,ko;q=0.9"
            }
    
    raw = requests.get(coupang_url, headers=header) 
    search = BeautifulSoup(raw.text, 'html.parser')

    box = search.find('ul', {'id' : 'productList'})
    all_product = box.find_all('li', {'class': 'search-product'})

    for product in all_product:
        imagefind = product.find("img", {'class' : 'search-product-wrap-img'})

        if imagefind.get("data-img-src") is None:
            imageLink = "http:" + imagefind.get('src')
        else:
            imageLink = "http:" + imagefind.get("data-img-src")

        title = product.find('div', {'class' : 'name'})
        price = product.find('strong', {'class' : 'price-value'})
        point = product.find('span', {'class' : 'rating-total-count'})
        
        if point is None:
                point=''

        link2 = product.find('a')['href']
        link = "https://www.coupang.com" + link2

        imageLink_list.append(imageLink)

        title_text = f"{product_num}. {title.text.strip()}"

        title_list.append(title_text)
        price_list.append(price.text)

        if isinstance(point, str):
                point_list.append(point)
        else:
                point_list.append(point.text)
        
        link_list.append(link)    
        product_num += 1
        
    keyword_submit()
    command_current()


win=Tk()
win.title("coupang shopping")       
win.geometry("710x800")


information0 = Label(win, text=f"<쿠팡 쇼핑 시스템>\n")         
information0.grid(column=1, row=0)

information1 = Label(win, text="아래 검색어를 입력하세요.")
information2 = Label(win, text="페이지 수 입력하세요.")

information1.grid(column=0, row=1)
information2.grid(column=1, row=1)

keyword_entry = Entry(win)
page_num_entry = Entry(win)

keyword_entry.grid(column=0, row=2)
page_num_entry.grid(column=1, row=2)

search_button = Button(win, text="검색", command=search_action)
search_button.grid(column=2, row=2, columnspan=3)

btnPrev=Button(win, text="<<이전", command=clickPrev)
btnNext=Button(win, text="다음>>", command=clickNext)

information_list = Label(win, text="<검색어의 쇼핑 목록>")
information_list.grid(column=1, row=3)

label1 = Label(win)
display1 = Text(win, width=100, height=3, borderwidth=5)
display2 = Text(win, width=100, height=3, borderwidth=5)
display3 = Text(win, width=100, height=3, borderwidth=5)
display4 = Text(win, width=100, height=3, borderwidth=5)

information3 = Label(win, text=(
                                f"<사용 설명서>\n\n"
                                f"첫 번째 빈 항목에 검색어를 입력하고\n"
                                f"두 번째 빈 항목에 원하는 페이지를 입력하세요\n\n"
                                f"한 페이지당 보통 50개~70개 정도 검색 가능하며\n"
                                f"그 후 검색 버튼을 누르면 페이지마다 쇼핑 목록을 볼 수 있습니다\n"
                                )
                    )

label1.grid(column=1, row=4)

display1.grid(column=0, row=5, columnspan=4)
display2.grid(column=0, row=6, columnspan=4)
display3.grid(column=0, row=7, columnspan=4)
display4.grid(column=0, row=8, columnspan=4)

btnPrev.grid(column=0, row=9)
btnNext.grid(column=2, row=9)

information3.grid(column=1, row=10)

win.mainloop()