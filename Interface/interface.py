import tkinter as tk
from PIL import ImageTk, Image
import json
import web3
from web3 import Web3
import tkinter.ttk

with open('bitpharma.abi') as json_file:
    abi_ = json.loads(json_file.read())
    
with open('bitpharma.bin') as file:
    bin_ = file.read()

ganache_URL = "HTTP://127.0.0.1:7545"
w3 = Web3(Web3.HTTPProvider(ganache_URL))

master=tk.Tk()
master.geometry('900x900')
master.title('Medical prescription Ethereum')

# Bitpharma login must be the first one, cannot acces other contracts 
def bitpharma_login(): 
    bitpharma_manager=str(id_entry.get())
    try:
        w3.eth.defaultAccount = bitpharma_manager
        contract = w3.eth.contract(bitpharma_manager, abi = abi_, bytecode = bin_)
        tx_hash=contract.constructor().transact() #deploy
        tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
        contract_address = tx_receipt['contractAddress'] ## address of the contract
        global contract_deployed
        contract_deployed = w3.eth.contract(address = contract_address, abi = abi_)
        bitpharma_window_()
        
    except web3.exceptions.InvalidAddress:
        text=tk.Label(master, text='You are not the BigPharma manager', 
                      bg ='sky blue', fg='red')
        text.grid(row=2, column=0, sticky='WE', padx=100, pady=10)

def init_whitelist():
    address=str(bitpharma_manager_entry.get())
    try:
        contract_deployed.functions.set_whitelist_address(address).transact() 
        text=tk.Label(bitpharma_window, text='Whitelist Set!', fg='green')
        text.grid(row=4, column=0, sticky='WE', padx=30, pady=10)
        subtitle=tk.Label(master, text='Contract deployed by BitPharma\n Login with your account:', 
                          bg ='sky blue', fg='green')
        subtitle.grid(row=2,column=0,sticky='WE', padx=100, pady=1) 
    except:
        text=tk.Label(bitpharma_window, text='Whitelist not set: insert a valid address!', fg='red')
        text.grid(row=4, column=0, sticky='WE', padx=30, pady=10)

def patient_login():
    try: 
        contract_deployed
        patient_account=str(id_entry.get())
        w3.eth.defaultAccount = patient_account
        patient_window_()
    except NameError:
        subtitle=tk.Label(master, text='Contract not deployed by BitPharma', 
                          bg ='sky blue', fg = 'red')
        subtitle.grid(row=2,column=0,sticky='WE', padx=100, pady=1) 

def purchase_prescription(): #Need to be fixed when working with prescriptions
    val_purchase = purchase_input.get().split(',')
    id_ = int(val_purchase[0])
    quantity_ = int(val_purchase[1])
    contract_deployed.functions.patient_purchasing(id_, quantity_).call()
    validate_purchase=contract_deployed.functions.patient_purchasing(id_, quantity_).call()
    print(validate_purchase)

def my_prescriptions(): #Need to be fixed when working with prescriptions
    address=str(id_entry.get())
    details=contract_deployed.functions.patient_prescriptions(address).transact()
    print(details)

def prescription_details(): #Need to be fixed when working with prescriptions
    id_prescr=int(prescr_details.get())
    details=contract_deployed.functions.prescription_details(id_prescr).transact()
    print(details)

def add_doctor():
    address=str(doctor_entry.get())
    try: 
        contract_deployed.functions.patient_add_reader(address).transact()
        val_text=tk.Label(patient_window, text='The doctor is add!', fg='green')
        val_text.grid(row=10, column=0, sticky='WE', padx=100, pady=10)
    except: 
        val_text=tk.Label(patient_window, text='The doctor is not add. Insert a valid address!', fg='red')
        val_text.grid(row=10, column=0, sticky='WE', padx=100, pady=10)

def remove_doctor():
    address=str(doctor_entry.get())
    try: 
        contract_deployed.functions.patient_remove_reader(address).transact()
        val_text=tk.Label(patient_window,text='The doctor is removed!', fg='green')
        val_text.grid(row=10, column=2, sticky='WE', padx=100, pady=10)
    except:
        val_text=tk.Label(patient_window,text='The doctor is not remove. Insert a valid address!', fg='red')
        val_text.grid(row=10, column=2, sticky='WE', padx=100, pady=10)      

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

def patient_window_():
    global patient_window
    patient_window=tk.Toplevel()
    patient_window.geometry('1200x1500')
    patient_window.title('Patient interface')

    # Background
    back_image = Image.open('background_patient.jpg')
    back_image = back_image.resize((1800,1500))
    background_image = ImageTk.PhotoImage(back_image)
    background_label = tk.Label(patient_window, image=background_image)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)
    background_label.image = background_image

    for col in range(3):
        patient_window.grid_columnconfigure(col, weight=1)
    for row in range(9):
        patient_window.grid_rowconfigure(row, weight=1)
    
    title=tk.Label(patient_window, text='Hello patient', font=30,  bg ='orange')
    title.grid(row=0, column=1, sticky='WE', padx=100, pady=10)
    title=tk.Label(patient_window, text='Here you can buy your medicine:', font=30,  bg ='orange')
    title.grid(row=1, column=1, sticky='WE', padx=100, pady=5)

    # Purchase 
    v = tk.StringVar(patient_window, value='id_prescription, quantity')
    global purchase_input
    purchase_input=tk.Entry(patient_window, justify=tk.CENTER, textvariable=v, 
                            fg = 'gray78', font = 'italic')
    purchase_input.grid(row=2, column=1, sticky='WE', padx=100, pady=10)

    purchase_button=tk.Button(patient_window, text='Purchase!', command=purchase_prescription,
                              fg="blue4", bg ='orange', bd=4, font="arial 18")
    purchase_button.grid(row=3, column=1, sticky='WE', padx=200, pady=10)

    # My prescriptions
    my_prescr = tk.Button(patient_window, text='My Prescriptions', command = my_prescriptions,
                          fg="blue4", bg ='orange', bd=4, font="arial 15")
    my_prescr.grid(row=5, column=0, sticky='WE', padx=100, pady=10)

    # Details prescription
    id_presc = tk.StringVar(patient_window, value='id_prescription')
    global prescr_details
    prescr_details=tk.Entry(patient_window, justify=tk.CENTER, textvariable=id_presc, 
                                  fg = 'gray78')
    prescr_details.grid(row=5, column=2, sticky='WE', padx=100, pady=10)
    button_details=tk.Button(patient_window, text='Details', command = prescription_details,
                             fg="blue4", bg ='orange', bd=4, font="arial 15")
    button_details.grid(row=6, column=2, sticky='WE', padx=100, pady=10)
    
    # Doctors section
    tkinter.ttk.Separator(patient_window, orient='horizontal').grid(column=0,
        row=7, sticky='WE',padx=10, pady=10)
    doct_section = tk.Label(patient_window, text='Manage doctor access', font = 30, bg ='orange')
    doct_section.grid(row=7, column=1,sticky='WE', padx=100, pady=10) 
    tkinter.ttk.Separator(patient_window, orient='horizontal').grid(column=2,
        row=7, sticky='WE', padx=10, pady=10)   

    id_doct = tk.StringVar(patient_window, value='Doctor public id')
    global doctor_entry
    doctor_entry=tk.Entry(patient_window, justify=tk.CENTER, textvariable=id_doct, 
                              fg = 'gray78', font = 'italic')
    doctor_entry.grid(row=8, column=1, sticky='WE', padx=100, pady=10)

    # Add Doctor
    add_button=tk.Button(patient_window, text='Add Doctor', command = add_doctor,
                         fg="blue4", bg ='orange', bd=4, font="arial 15")
    add_button.grid(row=9, column=0, sticky='WE', padx=100, pady=10)

    # Remove Doctor
    add_button=tk.Button(patient_window, text='Remove Doctor', command = remove_doctor,
                         fg="blue4", bg ='orange', bd=4, font="arial 15")
    add_button.grid(row=9, column=2, sticky='WE', padx=100, pady=10)
    
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

def bitpharma_window_():
    global bitpharma_window
    bitpharma_window=tk.Toplevel()
    bitpharma_window.geometry('500x500')
    bitpharma_window.title('Admin interface')
    # Background
    back_image = Image.open('background_bitpharma.jpg')
    background_image = ImageTk.PhotoImage(back_image)
    background_label = tk.Label(bitpharma_window, image=background_image)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)
    background_label.image = background_image
    
    bitpharma_window.grid_columnconfigure(0, weight=1)
    for row in range(5):
        bitpharma_window.grid_rowconfigure(row, weight=1)
            
    title=tk.Label(bitpharma_window, text='Hello BitPharma Manger', font=30, bg ='sky blue')
    title.grid(row=0,column=0,sticky='WE', padx=100, pady=10)    
    
    ticker=tk.Label(bitpharma_window, text='Insert the whitelist address:', bg ='sky blue')
    ticker.grid(row=1,column=0,sticky='WE', padx=100, pady=10)

    global bitpharma_manager_entry
    bitpharma_manager_entry=tk.Entry(bitpharma_window, justify=tk.CENTER, show="*")
    bitpharma_manager_entry.grid(row=2, column=0, sticky='WE', padx=100, pady=10)
    
    deploy_button=tk.Button(bitpharma_window,text='Insert Contract Whitelist', command=init_whitelist,
                           fg="blue", bg ='sky blue', bd=4, font="arial 15")
    deploy_button.grid(row=3,column=0,sticky='WE',padx=100, pady=10)

master.grid_columnconfigure(0, weight=1)
for row in range(9):
    master.grid_rowconfigure(row, weight=1)

# Background
back_image = Image.open('background.jpg')
background_image = ImageTk.PhotoImage(back_image)
background_label = tk.Label(master, image=background_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)
background_label.image = background_image

title=tk.Label(master, text='Welcome to Medical prescription Ethereum!', font=30, bg ='sky blue')
title.grid(row=0, column=0, sticky='WE', padx=100,pady=10)   
  
frame = tk.Frame(master)
frame.grid(row=1, column=0)
canvas = tk.Canvas(frame, bg ='sky blue', width=200, height=200)
canvas.pack()
load = Image.open('logo_pharma.png')
load = load.resize((200, 200))
photoimage = ImageTk.PhotoImage(load)
canvas.create_image(100, 100, image=photoimage)

subtitle=tk.Label(master, text='Login with your key:', bg ='sky blue')
subtitle.grid(row=2,column=0,sticky='WE', padx=100, pady=1)
id_entry=tk.Entry(master, justify=tk.CENTER, show="*")
id_entry.grid(row=3,column=0,sticky='WE', padx=100, pady=10)

first_button=tk.Button(master,text='Access as doctor', command = window1,
                       bg ='sky blue', fg="dark green", bd=4, font="arial 15")
first_button.grid(row=4,column=0,sticky='WE',padx=100, pady=10,)

second_button=tk.Button(master, text='Access as patient',command = patient_login,
                        bg ='sky blue', fg="dark green", bd=4, font="arial 15")
second_button.grid(row=5,column=0,sticky='WE',padx=100,pady=10)

third_button=tk.Button(master, text='Access as pharma',command = window3,
                       bg ='sky blue', fg="dark green", bd=4, font="arial 15")
third_button.grid(row=6,column=0,sticky='WE',padx=100, pady=10)

fourth_button=tk.Button(master, text='Access as BitPharma Manger', command = bitpharma_login,
                        bg ='sky blue', fg="dark green", bd=4, font="arial 15")
fourth_button.grid(row=7,column=0,sticky='WE',padx=100,pady=10)

if __name__=='__main__':
    master.mainloop()
