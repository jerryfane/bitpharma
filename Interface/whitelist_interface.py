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
master.geometry('1500x500')
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
    text.grid(row=3,column=2,sticky='WE', padx=30,pady=10)

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
        val_text=tk.Label(master,text='The doctor is registered!')
        val_text.grid(row=6,column=1,sticky='WE', padx=30,pady=10)
    else:
        val_text=tk.Label(master,text='The doctor is not registered!')
        val_text.grid(row=6,column=1,sticky='WE', padx=30,pady=10)

def check_pharma():
    address=str(pharma.get())
    validate_pharma=contract_deployed.functions.pharmacies(address).call()
    if validate_pharma:
        val_text=tk.Label(master,text='The Pharmacy is registered!')
        val_text.grid(row=8,column=1,sticky='WE', padx=30,pady=10)
    else:
        val_text=tk.Label(master,text='The Pharmacy is not registered!')
        val_text.grid(row=8,column=1,sticky='WE', padx=30,pady=10)
        
for column in range(3):
    master.grid_columnconfigure(column,weight=1)
for row in range(9):
    master.grid_rowconfigure(row, weight=1)
    

title=tk.Label(master, text='Welcome to Medical prescription Ethereum!', font=(30))
title.grid(row=0,column=0,columnspan=3,sticky='WE', padx=10,pady=(10))  
   
load = Image.open('logo_pharma.png')
load = load.resize((200, 200), Image.ANTIALIAS)
render = ImageTk.PhotoImage(load)
img = tk.Label(master, image=render)
img.image = render
img.grid(row=1, column=0,columnspan=3)

subtitle=tk.Label(master, text='Bitpharma address')
subtitle.grid(row=2,column=0,columnspan=2,sticky='WE', padx=50,pady=10)

bitpharma_manager_entry=tk.Entry(master,justify=tk.CENTER)
bitpharma_manager_entry.grid(row=3,column=0,sticky='WE', padx=50,pady=10)

deploy_button=tk.Button(master,text='Init Whitelist', command=init_whitelist)
deploy_button.grid(row=3,column=1,sticky='WE',padx=200)

subtitle=tk.Label(master, text='Manage users')
subtitle.grid(row=4,column=0,columnspan=2,sticky='WE', padx=10)

doc=tk.Entry(master,justify=tk.CENTER)
doc.grid(row=5,column=0,sticky='WE', padx=50,pady=10)

add_doctor_button=tk.Button(master, text='Add doctor',command=add_doctor)
add_doctor_button.grid(row=5,column=1,sticky='WE',padx=200,pady=(10))

check_doctor_button=tk.Button(master, text='Check doctor',command=check_doctor)
check_doctor_button.grid(row=5,column=2,sticky='WE',padx=200,pady=(10))

pharma=tk.Entry(master,justify=tk.CENTER)
pharma.grid(row=7,column=0,sticky='WE', padx=50,pady=10)

add_pharma_button=tk.Button(master, text='Add pharmacy',command=add_pharma)
add_pharma_button.grid(row=7,column=1,sticky='WE',padx=200,pady=10)

check_pharma_button=tk.Button(master, text='Check Pharmacy',command=check_pharma)
check_pharma_button.grid(row=7,column=2,sticky='WE',padx=200,pady=(10))

if __name__=='__main__':
    master.mainloop()
