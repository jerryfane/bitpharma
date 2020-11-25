import tkinter as tk
from PIL import ImageTk, Image

master=tk.Tk()
master.geometry('900x800')
master.title('Medical prescription Ethereum')
master.grid_columnconfigure(0,weight=1)
for row in range(4):
    master.grid_rowconfigure(row, weight=1)
    
def window1():
    window=tk.Tk()
    window.geometry('600x600')
    window.title('Doctor interface')
    for col in range(3):
        window.grid_columnconfigure(col, weight=1)
    for row in range(4):
        window.grid_rowconfigure(row, weight=1)
    

    title=tk.Label(window, text='Hello doctor!', font=(30))
    title.grid(row=0,column=1,sticky='N', padx=10,pady=10)
    
    ticker=tk.Label(window, text='Insert something')
    ticker.grid(row=1,column=1,sticky='WE', padx=10,pady=10)
    
    ticker_input=tk.Entry(window,justify=tk.CENTER)
    ticker_input.grid(row=2,column=1,sticky='WE', padx=100,pady=10)
    
    BS_button=tk.Button(window, text='Do things')
    BS_button.grid(row=4,column=1,sticky='WE', padx=40,pady=10)
    
def window2():
    window2=tk.Tk()
    window2.geometry('500x500')
    window2.title('Patient interface')
    window2.grid_columnconfigure(0,weight=1)
    for row in range(4):
        window2.grid_rowconfigure(row, weight=1)
    
    title=tk.Label(window2, text='Hello patient', font=(30))
    title.grid(row=0,column=0,sticky='N', padx=10,pady=10)
    
    ticker=tk.Label(window2, text='Insert something')
    ticker.grid(row=1,column=0,sticky='WE', padx=10,pady=10)
    
    ticker_input=tk.Entry(window2,justify=tk.CENTER)
    ticker_input.grid(row=2,column=0,sticky='WE', padx=200,pady=10)
    
    button=tk.Button(window2, text='Do something')
    button.grid(row=3,column=0,sticky='WE', padx=200,pady=10)
    
def window3():
    window3=tk.Tk()
    window3.geometry('500x500')
    window3.title('Pharma interface')
    for col in range(3):
        window3.grid_columnconfigure(col, weight=1)
    for row in range(5):
        window3.grid_rowconfigure(row, weight=1)
            
    title=tk.Label(window3, text='Hello pharma', font=(30))
    title.grid(row=0,column=0,columnspan=2,sticky='N')    
    
    ticker=tk.Label(window3, text='Insert something')
    ticker.grid(row=1,column=0,sticky='WE')
    
    ticker_input=tk.Entry(window3,justify=tk.CENTER)
    ticker_input.grid(row=2,column=0,sticky='WE', padx=200,pady=10)
    
    button=tk.Button(window3, text='Do something')
    button.grid(row=3,column=0,columnspan=2,rowspan=2,sticky='WE',padx=200,\
                pady=(0,30))
    
title=tk.Label(master, text='Welcome to Medical prescription Ethereum!', font=(30))
title.grid(row=0,sticky='WE', padx=10,pady=(10))     
load = Image.open('logo_pharma.png')
render = ImageTk.PhotoImage(load)
img = tk.Label(master, image=render)
img.image = render
img.grid(row=1, column=0)

subtitle=tk.Label(master, text='Here you can order all your meth!')

subtitle.grid(row=2,sticky='WE', padx=10,pady=(10))
first_button=tk.Button(master,text='Access as doctor', command=window1)
first_button.grid(row=3,column=0,sticky='WE',padx=300)

second_button=tk.Button(master, text='Access as patient',command=window2)
second_button.grid(row=4,column=0,sticky='WE',padx=300,pady=(10))

third_button=tk.Button(master, text='Access as pharma',command=window3)
third_button.grid(row=5,column=0,sticky='WE',padx=300,pady=(10,30))

if __name__=='__main__':
    master.mainloop()
