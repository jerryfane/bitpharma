import tkinter as tk
from PIL import ImageTk, Image
import json
from web3 import Web3

with open('bitpharma_wl.abi') as json_file:
    abi_ = json.loads(json_file.read())
    
with open('bitpharma_wl.bin') as file:
    bin_ = file.read()

ganache_URL = "HTTP://127.0.0.1:7545"
w3 = Web3(Web3.HTTPProvider(ganache_URL))

master=tk.Tk()
master.geometry('1500x600')
master.title('Medical prescription Ethereum')

def init_whitelist():
    bitpharma_manager=str(bitpharma_manager_entry.get())
    w3.eth.defaultAccount = bitpharma_manager
    contract = w3.eth.contract(bitpharma_manager, abi = abi_, bytecode = bin_)
    tx_hash=contract.constructor().transact() #deploy
    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    contract_address = tx_receipt['contractAddress'] ## address of the contract
    global contract_deployed
    contract_deployed = w3.eth.contract(address = contract_address, abi = abi_)

    text=tk.Label(master,text='Deployed!')
    text.grid(row=3, column=2, sticky='WE', padx=30, pady=10)

def add_doctor():
    address=str(doc.get())
    contract_deployed.functions.add_doctor(address).transact()

def add_pharma():
    address=str(pharma.get())
    contract_deployed.functions.add_pharmacy(address).transact()

def check_doctor():
    address=str(doc.get())
    validate_doctor=contract_deployed.functions.doctors(address).call()
    if validate_doctor:
        val_text=tk.Label(master,text='The doctor is registered!', fg='green')
        val_text.grid(row=6, column=1, sticky='WE', padx=30, pady=10)
    else:
        val_text=tk.Label(master,text='The doctor is not registered!', fg='red')
        val_text.grid(row=6, column=1, sticky='WE', padx=30, pady=10)

def check_pharma():
    address=str(pharma.get())
    validate_pharma=contract_deployed.functions.pharmacies(address).call()
    if validate_pharma:
        val_text=tk.Label(master,text='The Pharmacy is registered!', fg='green')
        val_text.grid(row=8, column=1, sticky='WE', padx=30, pady=10)
    else:
        val_text=tk.Label(master,text='The Pharmacy is not registered!', fg='red')
        val_text.grid(row=8, column=1, sticky='WE', padx=30, pady=10)

for column in range(3):
    master.grid_columnconfigure(column, weight=1)
for row in range(9):
    master.grid_rowconfigure(row, weight=1)
    
back_image = Image.open('pharmacy.jpg')
background_image = ImageTk.PhotoImage(back_image)
background_label = tk.Label(master, image=background_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)
background_label.image = background_image

title=tk.Label(master, text='Welcome to Medical prescription Ethereum!', font=30, fg="green")
title.grid(row=0,column=1,sticky='WE', padx=10, pady=(10))  

frame = tk.Frame(master)
frame.grid(row=1, column=1)
canvas = tk.Canvas(frame, bg="black", width=200, height=200)
canvas.pack()
load = Image.open('logo_pharma.png')
load = load.resize((200, 200))
photoimage = ImageTk.PhotoImage(load)
canvas.create_image(100, 100, image=photoimage)


subtitle=tk.Label(master, text='Bitpharma address:', fg='green', font="arial 8")
subtitle.grid(row=2, column=0, sticky='WE', padx=100, pady=10)

bitpharma_manager_entry=tk.Entry(master,justify=tk.CENTER, show="*")
bitpharma_manager_entry.grid(row=3, column=0, sticky='WE', padx=100, pady=10)

deploy_button=tk.Button(master,text='Initalize Whitelist', command=init_whitelist,
                        fg="green", bd=4, font="arial 15")
deploy_button.grid(row=3, column=1, sticky='WE', padx=100)

subtitle=tk.Label(master, text='Manage users:', fg='green', font="arial 8")
subtitle.grid(row=4, column=0, sticky='WE', padx=100)

doc=tk.Entry(master,justify=tk.CENTER, show="*")
doc.grid(row=5, column=0, sticky='WE', padx=100, pady=10)

add_doctor_button=tk.Button(master, text='Add doctor', command=add_doctor,
                            fg="green", bd=4, font="arial 15")
add_doctor_button.grid(row=5, column=1, sticky='WE', padx=100, pady=10)

check_doctor_button=tk.Button(master, text='Check doctor', command=check_doctor, 
                              fg="green", bd=4, font="arial 15")
check_doctor_button.grid(row=5, column=2, sticky='WE', padx=100, pady=10)

pharma=tk.Entry(master, justify=tk.CENTER, show="*")
pharma.grid(row=7, column=0, sticky='WE', padx=100, pady=10)

add_pharma_button=tk.Button(master, text='Add pharmacy',command=add_pharma, 
                            fg="green", bd=4, font="arial 15")
add_pharma_button.grid(row=7, column=1, sticky='WE', padx=100, pady=10)

check_pharma_button=tk.Button(master, text='Check Pharmacy',command=check_pharma,
                              fg="green", bd=4, font="arial 15")
check_pharma_button.grid(row=7, column=2, sticky='WE', padx=100, pady=(10))

if __name__=='__main__':
    master.mainloop()
