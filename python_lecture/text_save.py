from tkinter import *

def save():
    instr = entry.get()

    f = open("data4.txt", "w", encoding='utf-8')

    f.writelines(instr + "\n")

    print("저장됨")

    f.close()
    
win = Tk()
win.geometry("400x300")

entry=Entry(win)
entry.pack()

btt=Button(win, text="저장", command=save)
btt.pack()

win.mainloop()