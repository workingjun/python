from tkinter import *
import tkinter.messagebox as msg
from PIL import Image, ImageTk
from urllib.request import urlopen
from io import BytesIO
import requests
from bs4 import BeautifulSoup

num=0

def clickNext():
    global num
    global link_list
    global imageLink_list
    global title_list
    global price_list
    global point_list

    num+=1
    if num>len(imageLink_list):
        num=0

    image_url = imageLink_list[num]

    with urlopen(image_url) as response:
        image_data = response.read()
        image = Image.open(BytesIO(image_data))
        photo = ImageTk.PhotoImage(image)

    lable1.configure(image=photo)
    lable1.image=photo

    display1.delete(1.0, END)
    display2.delete(1.0, END)
    display3.delete(1.0, END)
    display4.delete(1.0, END)

    display1.insert(1.0, title_list[num])
    display2.insert(1.0, price_list[num])
    display3.insert(1.0, point_list[num])
    display4.insert(1.0, link_list[num])

def clickPrev():
    global num
    global num
    global link_list
    global imageLink_list
    global title_list
    global price_list
    global point_list

    num-=1
    if num<0:
        num = len(imageLink_list)
        
    image_url = imageLink_list[num]

    with urlopen(image_url) as response:
        image_data = response.read()
        image = Image.open(BytesIO(image_data))
        photo = ImageTk.PhotoImage(image)

    lable1.configure(image=photo)
    lable1.image=photo
    
    display1.delete(1.0, END)
    display2.delete(1.0, END)
    display3.delete(1.0, END)
    display4.delete(1.0, END)
    
    display1.insert(1.0, title_list[num])
    display2.insert(1.0, price_list[num])
    display3.insert(1.0, point_list[num])
    display4.insert(1.0, link_list[num])

def search():
    global link_list
    global imageLink_list
    global title_list
    global price_list
    global point_list

    link_list=[]
    imageLink_list=[]
    title_list=[]
    price_list=[]
    point_list=[]

    search_query = keyword.get()
    page_num = 1

    while page_num<2:
        keyword.get()
        coupang_url = 'https://www.coupang.com/np/search?q='+ search_query + '&channel=user&component=&eventCategory=SRP&trcid=&traid=&sorter=scoreDesc&minPrice=&maxPrice=&priceRange=&filterType=&listSize=36&filter=&isPriceRange=false&brand=&offerCondition=&rating=0&page='+ str(page_num)+'&rocketAll=false&searchIndexingToken=1=9&backgroundColor='

        header={'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36", 
        "Accept-Language": "ko-KR"}

        raw = requests.get(coupang_url, headers=header) 
        search = BeautifulSoup(raw.text, 'html.parser')


        box = search.find('ul', {'id' : 'productList'})
        all_product = box.find_all('li', {'class': 'search-product'})

        count=0
        
        for index, product in enumerate(all_product):
            image = product.find("img")
            imageLink = image.get("src")
            imageLink= "https:"+ imageLink
            title = product.find('div', {'class' : 'name'})
            price = product.find('strong', {'class' : 'price-value'})
            point = product.find('span', {'class' : 'rating-total-count'})
            link2 = product.find('a')['href']
            link = "https://www.coupang.com" + link2
            
            count += 1

            imageLink_list.append(imageLink)
            title_list.append(title.text)
            price_list.append(price.text)
            point_list.append(point.text)
            link_list.append(link)
            
            if count==5:
                    break
        page_num+=1


win=Tk()
win.geometry("800x600")

keyword = Entry(win, text="검색어를 입력하세요")
keyword.pack()
search_button = Button(win, text="검색", command=search)
search_button.pack()

btnPrev=Button(win, text="<<이전", command=clickPrev)
btnNext=Button(win, text="다음>>", command=clickNext)

lable1 = Label(win)
display1 = Text(win, width=30, height=3, borderwidth=5)
display2 = Text(win, width=30, height=3, borderwidth=5)
display3 = Text(win, width=30, height=3, borderwidth=5)
display4 = Text(win, width=30, height=3, borderwidth=5)


btnPrev.pack()
btnNext.pack()
lable1.pack()
display1.pack()
display2.pack()
display3.pack()
display4.pack()

# display1.grid(row=0, column=0)
# display2.grid(row=0, column=1)
# display3.grid(row=1, column=0)
# display4.grid(row=1, column=1)

win.mainloop()