import argparse
from tkinter import *
from tkinter import ttk  

def clicked(num):
    if texts[num] == "0":
        buttons[num].configure(text = "1")
        texts[num] = "1"
    else:
        buttons[num].configure(text = "0")
        texts[num] = "0"

window = Tk()
window.title("graphEdit")
window.geometry('1080x920') #1080 - x, 920 - y
window.resizable(False, False)
tab_control = ttk.Notebook(window) 
tab1 = ttk.Frame(tab_control)  
tab2 = ttk.Frame(tab_control) 
tab3 = ttk.Frame(tab_control) 
tab_control.add(tab1, text='Editing')  
tab_control.add(tab2, text='Run Solutions')  
tab_control.add(tab3, text='File')
buttons = []
texts = []
n = 5
for i in range(0, n):
    for j in range(0, n):
        buttons.append( Button( tab1, text="0", command=lambda num=i*n+j: clicked(num) ) )
        buttons[i*n+j].place(x = 75+j*(1080-150)//n, y = 75+i*(920-150)//n, width = (1080-150)//n, height = (920-150)//n)
        texts.append("0")

tab_control.pack(expand=1, fill='both')  
window.mainloop()