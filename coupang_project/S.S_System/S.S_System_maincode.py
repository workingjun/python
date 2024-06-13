from tkinter import ttk
import tkinter as tk
from tkinter import messagebox

from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess
import chromedriver_autoinstaller

from PIL import Image, ImageTk
from urllib.request import urlopen
from io import BytesIO
import webbrowser

from Class_1_Searching_blogs import BlogManager
from Class_2_Searching_coupang import Setting_Options
from Class_3_Shopping_coupang import ShopManager
from Class_4_sorting import SortManager
from Class_5_Searching_review import ReviewManager

index_num = 0

display4 = None
scrollbar_display4 = None
driver=None

############################################################################################
def start_chrome_and_driver():
    global driver, chrome_process, blog_search_data, coupang_list, coupang_rev, coupang, coupang_st

    messagebox.showinfo("크롬 실행", "크롬이 실행 중입니다. 잠시만 기다려 주세요.")
    try:
        chrome_path = (
            r'C:\Program Files\Google\Chrome\Application\chrome.exe '
            r'--remote-debugging-port=9221 --user-data-dir="C:\chrometemp" '
            r'--window-size=500,1000 --window-position=-5,-5 '
        )

        chrome_process = subprocess.Popen(chrome_path)
    except FileNotFoundError:
        chrome_path = (
            r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe '
            r'--remote-debugging-port=9221 --user-data-dir="C:\chrometemp" '
            r'--window-size=500,1000 --window-position=-5,-5 '
        )
        chrome_process = subprocess.Popen(chrome_path)

    options = webdriver.ChromeOptions()
    options.add_experimental_option("debuggerAddress", "127.0.0.1:9221")

    chromedriver_autoinstaller.install()
    driver = webdriver.Chrome(options=options)

    driver.get("https://coupang.com")

    blog_search_data=BlogManager(driver)
    coupang_rev = ReviewManager(driver)
    coupang = Setting_Options(driver)
    coupang_st = SortManager()
    coupang_list = ShopManager(driver)

def chrome_close():
    global driver

    messagebox.showinfo("크롬 닫기", "정말로 크롬을 닫으시겠습니까?")
    try:
        driver=None
        chrome_process.terminate()
    except:
        messagebox.showinfo("크롬 미실행", "크롬을 찾지 못했습니다.")

def delete_and_insert():
    display1.config(state=tk.NORMAL)
    display2.config(state=tk.NORMAL)
    display3.config(state=tk.NORMAL)
   
    display1.delete(1.0, tk.END)
    display2.delete(1.0, tk.END)
    display3.delete(1.0, tk.END)
  
    display1.insert(1.0, "[제품 이름]\n")
    display2.insert(1.0, "[가격]\n")
    display3.insert(1.0, "[리뷰 갯수]\n")
    
    display1.insert(2.0, title_list[index_num])
    display2.insert(2.0, price_list[index_num])
    display3.insert(2.0, point_list[index_num])

    display1.config(state=tk.DISABLED)
    display2.config(state=tk.DISABLED)
    display3.config(state=tk.DISABLED)
    
def blog_delete_and_insert():
    global blog_title_list, blog_contents_list, blog_username, blog_index_num
    
    ## 텍스트에 삽입하거나 삭제하기 
    display5.delete(1.0, tk.END)
    display6.delete(1.0, tk.END)
    display7.delete(1.0, tk.END)

    display5.insert(1.0, "[블로그 제목]\n")
    display6.insert(1.0, "[블로그 내용]\n")
    display7.insert(1.0, "[블로그 주인장]\n")

    display5.insert(2.0, blog_title_list[blog_index_num])
    display6.insert(2.0, blog_contents_list[blog_index_num])
    display7.insert(2.0, blog_username[blog_index_num])

def open_link():
    webbrowser.open(link_list[index_num])

def img_insert():
    image_url = imageLink_list[index_num]
    try:
        with urlopen(image_url) as response:
            image_data = response.read()
            image = Image.open(BytesIO(image_data))
            photo = ImageTk.PhotoImage(image)
        label1.configure(image=photo)
        label1.image = photo
    except:
        label1.configure(image='')
        label1.image = None
        messagebox.showinfo("청소년 이용 불가", "본 상품은 만 19세 미만의 청소년이 이용할 수 없습니다.")

def blog_keyword_submit():
    ## 어떤 블로그 목록인지 
    keyword_got2 = keyword_entry2.get()
    keyword_got2 = f"<{keyword_got2}에 대한 블로그>"
    blog_information_list.configure(text=keyword_got2)
    
def keyword_submit():
    keyword_got = keyword_entry.get()
    information_list.config(text=f"<{keyword_got}의 쇼핑 목록>")

def blog_command_current():
    global blog_index_num

    blog_index_num=0

    blog_delete_and_insert()

def BlogclickNext():
    global blog_index_num, blog_username
        
    blog_index_num+=1
    if blog_index_num>len(blog_username)-1:
        blog_index_num=0
        
    blog_delete_and_insert()

def BlogclickPrev():
    global blog_index_num, blog_username

    blog_index_num-=1
    if blog_index_num<0:
        blog_index_num = len(blog_username)-1
    
    blog_delete_and_insert()

def command_current():
    global index_num
    index_num = 0
    img_insert()
    delete_and_insert()

def clickNext():
    global index_num

    index_num += 1
    if index_num > len(imageLink_list) - 1:
        index_num=0

    img_insert()
    delete_and_insert()
    display4_forget()

def clickPrev():
    global index_num

    index_num -= 1
    if index_num < 0:
        index_num = len(imageLink_list) - 1

    img_insert()
    delete_and_insert()
    display4_forget()

def display4_forget():
    if display4:
        display4.grid_forget()
    if scrollbar_display4:
        scrollbar_display4.grid_forget()

def review_link():
    global display4, scrollbar_display4

    messagebox.showinfo("크롤링 진행 중", "리뷰를 가져오는 중입니다. 잠시 기다려주세요...")

    re5 = coupang_rev.Loading_reviews(link_list[index_num], 5)
    
    scrollbar_display4 = ttk.Scrollbar(scrollable_frame)
    display4 = tk.Text(scrollable_frame, width=80, height=30, borderwidth=5, yscrollcommand=scrollbar_display4.set)
    scrollbar_display4.config(command=display4.yview)
    
    display4.grid(column=0, row=12, columnspan=4, pady=5)
    scrollbar_display4.grid(column=4, row=12, sticky='ns')
    
    display4.config(state=tk.NORMAL)
    display4.delete(1.0, tk.END)
    display4.insert(1.0, "[최고리뷰 내용]\n")
    display4.insert(2.0, re5[0])
    display4.config(state=tk.DISABLED)

def Options_list():
    search_query = keyword_entry.get()
    
    try:
        xpath = "//div[@class='main-today__img-container c1-image']"
        driver.find_element(By.XPATH, xpath)
    except:
        pass
    else:
        coupang.getting_keyword(search_query)

    try:
        xpath="//div[@class='prod-image__items']"
        driver.find_element(By.XPATH, xpath)
    except:
        pass
    else:
        driver.get("http://coupang.com/")
        coupang.getting_keyword(search_query)

    try:
        xpath = "//div[contains(@class, 'search-filter-options search-')]"
        driver.find_elements(By.XPATH, xpath)
    except:
        pass
    else:
        option_names = coupang.print_Option_names()
    
    return option_names

def option_selected(options, opt=None):
    try:
        coupang.Click_option(options, opt)
    except:
        pass
    
def update_options():
    messagebox.showinfo("크롤링 진행 중", "옵션을 가져오는 중입니다. 잠시 기다려주세요...")

    options = Options_list()
    
    for i in range(4):
        var = globals()[f"var{i+1}"]
        option_menu = ttk.OptionMenu(scrollable_frame, var, var.get(), *options, 
                                command=lambda opt=options ,i=i, j=3: 
                                (option_selected(options=opt), update_option_items(i, j)))
        option_menu.grid(column=i, row=3, padx=5, pady=5)

    for i in range(4, 8):
        var = globals()[f"var{i+1}"]
        option_menu = ttk.OptionMenu(scrollable_frame, var, var.get(), *options, 
                                command=lambda opt=options ,i=i, j=5: 
                                (option_selected(options=opt), update_option_items(i, j)))
        option_menu.grid(column=i-4, row=5, padx=5, pady=5)

def update_option_items(i, j):
    options = coupang.print_Option_items(globals()[f"var{i+1}"].get())
    
    var = globals()[f"var_sub_{i+1}"]
    option_menu2 = ttk.OptionMenu(scrollable_frame, var, var.get(), *options, 
                              command=lambda opt=options, i=i: 
                              option_selected(options=globals()[f"var{i+1}"].get(), opt=opt))
    if i>=4:
        i = i - 4
    option_menu2.grid(column=i, row=j+1, padx=5, pady=5)

def search_action():
    global link_list, imageLink_list, title_list, price_list, point_list
    
    messagebox.showinfo("크롤링 진행 중", "검색 결과를 가져오는 중입니다. 잠시 기다려주세요...")

    search_query = keyword_entry.get()
    
    if driver==None:
        messagebox.showinfo("크롬 미실행", "크롬을 실행한 뒤에 검색버튼을 누르세요.")
        
    try:
        page_num = int(page_num_entry.get())
    except:
        page_num = 1
    
    try:
        xpath = "//div[@class='main-today__img-container c1-image']"
        driver.find_element(By.XPATH, xpath)
    except:
        pass
    else:
        coupang.getting_keyword(search_query)

    try:
        xpath="//div[@class='prod-image__items']"
        driver.find_element(By.XPATH, xpath)
    except:
        pass
    else:
        driver.get("http://coupang.com/")
        coupang.getting_keyword(search_query)

    try:
        xpath = "//div[contains(@class, 'search-filter-options search-')]"
        driver.find_elements(By.XPATH, xpath)
    except:
        pass
    else:
        link_list, imageLink_list, title_list, price_list, point_list = [], [], [], [], []

        link_list, imageLink_list, title_list, price_list, point_list = coupang_list.find_html(page_num)
        
        sorting()
        keyword_submit()
        command_current()
        grid_data()
        display4_forget()

def search_Blog():
    global blog_title_list, blog_contents_list, blog_username, blog_search_data

    blog_title_list, blog_contents_list, blog_username=[], [], []
    
    messagebox.showinfo("크롤링 진행 중", "블로그 검색 결과를 가져오는 중입니다. 잠시 기다려주세요...")
    
    blog_search_data.Search_and_Scroll(keyword_entry2.get())
    blog_username, blog_title_list, blog_contents_list = blog_search_data.find_html()  
        
    blog_keyword_submit()
    blog_command_current()

def sorting():
    coupang_list=[]
    global link_list, imageLink_list, title_list, price_list, point_list

    for i in range(len(price_list)):
        coupang_list.append([link_list[i], imageLink_list[i], title_list[i], price_list[i], point_list[i]])

    coupang_list = coupang_st.sorting(coupang_list)

    link_list, imageLink_list, title_list, price_list, point_list = [], [], [], [], []

    for i in range(len(coupang_list)):
        link_list.append(coupang_list[i][0])
        imageLink_list.append(coupang_list[i][1])
        title_list.append(coupang_list[i][2])
        price_list.append(coupang_list[i][3])
        point_list.append(coupang_list[i][4])

def grid_data():
    information_list.grid(column=1, row=7, columnspan=2, pady=5)
    label1.grid(column=1, row=8, columnspan=2, pady=5)
    display1.grid(column=0, row=9, columnspan=4, pady=5)
    display2.grid(column=0, row=10, columnspan=2, pady=5)
    display3.grid(column=2, row=10, columnspan=2, pady=5)
    
    link_button.grid(column=0, row=13, pady=5)
    rev_button.grid(column=3, row=13, pady=5)

    btnPrev.grid(column=0, row=14, pady=5)
    btnNext.grid(column=3, row=14, pady=5)
    
def reset():
    global link_list, imageLink_list, title_list, price_list, point_list
    
    driver.get("https://coupang.com/")
    messagebox.showinfo("리셋 완료", "리셋되었습니다. 다시 검색해주세요.")

    link_list, imageLink_list, title_list, price_list, point_list = [], [], [], [], []
    
    display1.grid_forget()
    display2.grid_forget()
    display3.grid_forget()
    display4_forget()

    for i in range(8):
        globals()[f"var_sub_{i+1}"].set("선택없음")
        globals()[f"var{i+1}"].set("선택없음")
    
    for i in range(4):
        option_menu = ttk.OptionMenu(scrollable_frame, globals()[f"var{i+1}"], '선택없음')
        option_menu.grid(column=i, row=3, padx=5, pady=5)

        option_menu2 = ttk.OptionMenu(scrollable_frame, globals()[f"var_sub_{i+1}"], '선택없음')
        option_menu2.grid(column=i, row=4, padx=5, pady=5)

def _on_mouse_wheel(event):
    canvas.yview_scroll(int(-1*(event.delta/120)), "units")

def show_window(event=None):
    global driver

    selected_tab = tab.select()
    selected_tab_index = tab.index(selected_tab)
    print(f"Tab changed to {selected_tab_index + 1}")


    if selected_tab_index ==0:
        try:
            driver.get("https://coupang.com")
            print("첫번째 탭 입력됨")
        except:
            pass
    elif selected_tab_index ==1:
        try:
            driver.get("https://naver.com")
            print("두번째 탭 입력됨")
        except:
            pass

def disable_event(event):
    return "break"


def quit_program():
    answer= messagebox.askyesno("종료", "정말로 종료하시겠습니까?")

    if answer:
        win.destroy()
    else:
        pass

################################################################################################

win = tk.Tk()
win.title("Coupang Shopping")
win.geometry("620x700+500+0")
#script_dir = os.getcwd()
#icon_path = os.path.join(script_dir,"shopping1.png")
#icon = tk.PhotoImage(file=icon_path)

#win.wm_iconphoto(False, icon)

###############################################################################################

tab=ttk.Notebook(win)
tab.bind("<<NotebookTabChanged>>", show_window)

tab1 = ttk.Frame(tab, style="Custom.TFrame")
tab.add(tab1, text="쿠팡 검색")

canvas = tk.Canvas(tab1)
scrollbar = ttk.Scrollbar(tab1, orient=tk.VERTICAL, command=canvas.yview)
scrollable_frame = ttk.Frame(canvas)

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")
    )
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

tab.pack(expand=True, fill='both')
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

information0 = ttk.Label(scrollable_frame, text="<쿠팡 쇼핑 시스템>\n")
start_button = ttk.Button(scrollable_frame, text="Chrome 실행", command=start_chrome_and_driver)
close_button = ttk.Button(scrollable_frame, text="Chrome 닫기", command=chrome_close)
information1 = ttk.Label(scrollable_frame, text="검색어 입력")
information2 = ttk.Label(scrollable_frame, text="페이지 숫자")
information3 = ttk.Label(scrollable_frame, text='옵션 선택')
information4 = ttk.Label(scrollable_frame, text='제품 검색')
keyword_entry = ttk.Entry(scrollable_frame, width=10)
page_num_entry = ttk.Entry(scrollable_frame, width=10)
select_options = ttk.Button(scrollable_frame, text="옵션", command=update_options)
search_button = ttk.Button(scrollable_frame, text="검색", command=search_action)
reset_button = ttk.Button(scrollable_frame, text="리셋", command=reset)
btnPrev = ttk.Button(scrollable_frame, text="<<이전", command=clickPrev)
btnNext = ttk.Button(scrollable_frame, text="다음>>", command=clickNext)
information_list = ttk.Label(scrollable_frame, text="<검색어의 쇼핑 목록>")
label1 = ttk.Label(scrollable_frame)
display1 = tk.Text(scrollable_frame, width=80, height=3, borderwidth=5)
display2 = tk.Text(scrollable_frame, width=39, height=3, borderwidth=5)
display3 = tk.Text(scrollable_frame, width=39, height=3, borderwidth=5)

display1.config(state=tk.DISABLED)
display2.config(state=tk.DISABLED)
display3.config(state=tk.DISABLED)

link_button = ttk.Button(scrollable_frame, text="Open Link", command=open_link)
rev_button = ttk.Button(scrollable_frame, text="review link", command=review_link)
instructions = ttk.Label(scrollable_frame,
    text=(
        "                      <사용 설명서>\n\n"
        "첫 번째 빈 항목에 검색어를 입력하고\n"
        "두 번째 빈 항목에 원하는 페이지를 입력하세요\n\n"
        "예) 2 : 두 번째 목록의 페이지\n\n"
        "한 페이지당 검색 가능한 물품을 볼 수 있으며\n"
        "또한 원하는 옵션을 차례로 선택하면\n"
        "페이지마다 쇼핑 목록을 볼 수 있습니다\n\n"
        "마지막으로 리셋을 통해 다시 세팅이 가능합니다"
    )
)

var1 = tk.StringVar(value="선택없음")
var2 = tk.StringVar(value="선택없음")
var3 = tk.StringVar(value="선택없음")
var4 = tk.StringVar(value="선택없음")
var5 = tk.StringVar(value="선택없음")
var6 = tk.StringVar(value="선택없음")
var7 = tk.StringVar(value="선택없음")
var8 = tk.StringVar(value="선택없음")

var_sub_1 = tk.StringVar(value="선택없음")
var_sub_2 = tk.StringVar(value="선택없음")
var_sub_3 = tk.StringVar(value="선택없음")
var_sub_4 = tk.StringVar(value="선택없음")
var_sub_5 = tk.StringVar(value="선택없음")
var_sub_6 = tk.StringVar(value="선택없음")
var_sub_7 = tk.StringVar(value="선택없음")
var_sub_8 = tk.StringVar(value="선택없음")

canvas.bind_all("<MouseWheel>", _on_mouse_wheel)
canvas.bind_all("<Button-4>", _on_mouse_wheel)
canvas.bind_all("<Button-5>", _on_mouse_wheel)

##############################################################################################

tab2 = ttk.Frame(tab)
tab.add(tab2, text="블로그 검색")

information5 = ttk.Label(tab2, text=f"<블로그 탐색>\n")         
keyword_entry2 = ttk.Entry(tab2, width=40)
search_button2 = ttk.Button(tab2, text="검색", command=search_Blog)
BlogbtnPrev=ttk.Button(tab2, text="<<이전", command=BlogclickPrev)   
BlogbtnNext=ttk.Button(tab2, text="다음>>", command=BlogclickNext)
blog_information_list=ttk.Label(tab2, text="<검색어의 블로그>")


display5 = tk.Text(tab2, width=80, height=6, borderwidth=5)
display7 = tk.Text(tab2, width=80, height=6, borderwidth=5)
display6 = tk.Text(tab2, width=80, height=6, borderwidth=5)

display5.bind("<Key>", disable_event)
display6.bind("<Key>", disable_event)
display7.bind("<Key>", disable_event)

display5.bind("<Button-1>", lambda event: display5.focus_set())  # 클릭 시 포커스 유지
display6.bind("<Button-1>", lambda event: display6.focus_set())  # 클릭 시 포커스 유지
display7.bind("<Button-1>", lambda event: display7.focus_set())

##############################################################################################

information0.grid(row=0, column=0, columnspan=2, pady=5)
start_button.grid(row=0, column=2, pady=5)
close_button.grid(row=0, column=3, pady=5)
information1.grid(row=1, column=0)
information2.grid(row=1, column=1)
information3.grid(row=1, column=2)
information4.grid(row=1, column=3)
keyword_entry.grid(row=2, column=0)
page_num_entry.grid(row=2, column=1)
select_options.grid(row=2, column=2)
search_button.grid(row=2, column=3)
reset_button.grid(column=1, row=13, columnspan=2, pady=5)
instructions.grid(column=1, row=15, columnspan=2, pady=5)

information5.grid(column=4, row=0)
keyword_entry2.grid(column=4, row=2)
search_button2.grid(column=6, row=2, columnspan=2)
blog_information_list.grid(column=4, row=3)
display5.grid(column=4, row=5, columnspan=4, pady=10)
display7.grid(column=4, row=8, columnspan=4, pady=10)
display6.grid(column=4, row=11, columnspan=4, pady=10)
BlogbtnPrev.grid(column=4, row=20, pady=10)
BlogbtnNext.grid(column=5, row=20, pady=10)

win.protocol("WM_DELETE_WINDOW", quit_program)
win.mainloop()

try:
    chrome_process.terminate()
except:
    pass
###################################################################################3