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
bitpharma_manager =  w3.eth.accounts[0]
w3.eth.defaultAccount = bitpharma_manager
contract = w3.eth.contract(bitpharma_manager, abi = abi_, bytecode = bin_)
tx_hash=contract.constructor().transact() #deploy
tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
contract_address = tx_receipt['contractAddress'] ## address of the contract
contract_deployed = w3.eth.contract(address = contract_address, abi = abi_)

master=tk.Toplevel()
master.geometry('900x800')
master.title('Medical prescription Ethereum')

def init_whitelist(bitpharma_manager):

    pass

def add_doctor(contract_deployed,address):
    contract_deployed.functions.doctors(address).transact()

for column in range(2):
    master.grid_columnconfigure(column,weight=1)
for row in range(4):
    master.grid_rowconfigure(row, weight=1)
    

title=tk.Label(master, text='Welcome to Medical prescription Ethereum!', font=(30))
title.grid(row=0,sticky='WE', padx=10,pady=(10))  
   
load = Image.open('logo_pharma.png')
render = ImageTk.PhotoImage(load)
img = tk.Label(master, image=render)
img.image = render
img.grid(row=1, column=0)

subtitle=tk.Label(master, text='Bitpharma address')
subtitle.grid(row=2,sticky='WE', padx=10,pady=(10))

ticker_input=tk.Entry(master,justify=tk.CENTER)
ticker_input.grid(row=3,column=0,sticky='WE', padx=100,pady=10)

first_button=tk.Button(master,text='Init Whitelist', command=init_whitelist(ticker_input.get()))
first_button.grid(row=4,column=0,sticky='WE',padx=300)

subtitle=tk.Label(master, text='Manage users')
subtitle.grid(row=5,sticky='WE', padx=10,pady=(10))

doc=tk.Entry(master,justify=tk.CENTER)
doc.grid(row=6,column=0,sticky='WE', padx=100,pady=10)

second_button=tk.Button(master, text='Add doctor',command=add_doctor(contract_deployed,doc.get()))
second_button.grid(row=7,column=0,sticky='WE',padx=300,pady=(10))

# third_button=tk.Button(master, text='Access as pharma',command=window3)
# third_button.grid(row=5,column=0,sticky='WE',padx=300,pady=(10,30))

if __name__=='__main__':
    master.mainloop()
