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

def doctor_login():
    try: 
        contract_deployed
        doc_account=str(id_entry.get())
        w3.eth.defaultAccount = doc_account
        doctor_window_()
    except NameError:
        subtitle=tk.Label(master, text='Contract not deployed by BitPharma', 
                          bg ='sky blue', fg = 'red')
        subtitle.grid(row=2,column=0,sticky='WE', padx=100, pady=1) 

def pharma_login():
    try: 
        contract_deployed
        pharma_account=str(id_entry.get())
        w3.eth.defaultAccount = pharma_account
        pharma_window_()
    except NameError:
        subtitle=tk.Label(master, text='Contract not deployed by BitPharma', 
                          bg ='sky blue', fg = 'red')
        subtitle.grid(row=2,column=0,sticky='WE', padx=100, pady=1) 

def patient_prescriptions_global(address):
    return contract_deployed.functions.patient_prescriptions(address).call()

def prescription_details_global(id_prescr):
    return contract_deployed.functions.prescription_details(id_prescr).call()

def doctor_window_():
    def prescribe_drug():
        drug=str(drug_input.get())
        quantity=int(quantity_input.get())
        maxclaim=int(maxclaim_input.get())
        purchaseCooldown =int(purchaseCooldown_input.get())
        daysToExpiration=int(daysToExpiration_input.get())
        patient=str(patient_address_input.get())
        contract_deployed.functions.newPrescription(drug,quantity,maxclaim,purchaseCooldown,daysToExpiration,patient).transact()
    
    def patient_prescriptions():
        address=str(patient_address_input2.get())
        details=patient_prescriptions_global(address)
        print(details)
 
    def prescription_details():
        _id=int(prescrId_input.get())
        details=prescription_details_global(_id)
        print(details)
        
    doctor_window=tk.Toplevel()
    doctor_window.geometry('1200x700')
    doctor_window.title('Doctor interface')
    for col in range(3):
        doctor_window.grid_columnconfigure(col, weight=1)
    for row in range(9):
        doctor_window.grid_rowconfigure(row, weight=1)
    
    title_doctor=tk.Label(doctor_window, text='Hello doctor!', font=(30))
    title_doctor.grid(row=0,column=1,sticky='N', padx=10,pady=10)
    
    subtitle_doctor=tk.Label(doctor_window, text='Here you can prescribe to your patients and \ncheck their prescriptions')
    subtitle_doctor.grid(row=1,column=1,sticky='WE', padx=10,pady=10)
    
    first_section=tk.Label(doctor_window, text='New Prescription')
    first_section.grid(row=2,column=1,sticky='WE', padx=10,pady=10)
    
    drug_input=tk.Entry(doctor_window,justify=tk.CENTER, textvariable=tk.StringVar(doctor_window,'drug'), 
                            fg = 'gray78', font = 'italic')
    drug_input.grid(row=3, column=0, sticky='WE', padx=100, pady=10)
    
    quantity_input=tk.Entry(doctor_window,justify=tk.CENTER, textvariable=tk.StringVar(doctor_window,'quantity'), 
                            fg = 'gray78', font = 'italic')
    quantity_input.grid(row=3, column=1, sticky='WE', padx=100, pady=10)
    
    maxclaim_input=tk.Entry(doctor_window,justify=tk.CENTER, textvariable=tk.StringVar(doctor_window,'maxclaim'), 
                            fg = 'gray78', font = 'italic')
    maxclaim_input.grid(row=3, column=2, sticky='WE', padx=100, pady=10)
    
    purchaseCooldown_input=tk.Entry(doctor_window,justify=tk.CENTER, textvariable=tk.StringVar(doctor_window,'purchaseCooldown'), 
                            fg = 'gray78', font = 'italic')
    purchaseCooldown_input.grid(row=4, column=0, sticky='WE', padx=100, pady=10)
    
    daysToExpiration_input=tk.Entry(doctor_window,justify=tk.CENTER, textvariable=tk.StringVar(doctor_window,'daysToExpiration'), 
                            fg = 'gray78', font = 'italic')
    daysToExpiration_input.grid(row=4, column=1, sticky='WE', padx=100, pady=10)
    
    patient_address_input=tk.Entry(doctor_window,justify=tk.CENTER, textvariable=tk.StringVar(doctor_window,'patient_address'), 
                            fg = 'gray78', font = 'italic')
    patient_address_input.grid(row=4, column=2, sticky='WE', padx=100, pady=10)
    
    prescribe_button=tk.Button(doctor_window, text='Prescribe',command = prescribe_drug)
    prescribe_button.grid(row=5,column=1,sticky='WE', padx=40,pady=10)
    
    tkinter.ttk.Separator(doctor_window, orient='horizontal').grid(column=0,
    row=6, sticky='WE',padx=10, pady=10,columnspan=3)
    
    second_section=tk.Label(doctor_window, text='Manage Prescriptions')
    second_section.grid(row=7,column=1,sticky='WE', padx=10,pady=10)
    
    patient_address_input2=tk.Entry(doctor_window,justify=tk.CENTER, textvariable=tk.StringVar(doctor_window,'patient_address'), 
                            fg = 'gray78', font = 'italic')
    patient_address_input2.grid(row=8, column=0, sticky='WE', padx=100, pady=10)
    
    check_patient_prescriptions_button=tk.Button(doctor_window, text='Check patient prescriptions',
                                                 command = patient_prescriptions)
    check_patient_prescriptions_button.grid(row=8,column=1,sticky='WE', padx=40,pady=10) 
    
    prescrId_input=tk.Entry(doctor_window,justify=tk.CENTER, textvariable=tk.StringVar(doctor_window,'prescription_ID'), 
                            fg = 'gray78', font = 'italic')
    prescrId_input.grid(row=9, column=0, sticky='WE', padx=100, pady=10)
    
    prescription_details_button=tk.Button(doctor_window, text='Check prescriptions details',
                                                 command = prescription_details)
    prescription_details_button.grid(row=9,column=1,sticky='WE', padx=40,pady=10)  
    

def patient_window_():
    def patient_prescriptions():
        address=str(id_entry.get())
        details=patient_prescriptions_global(address)
        print(details)
 
    def prescription_details():
        _id=int(prescr_details.get())
        details=prescription_details_global(_id)
        print(details)
        
    def add_doctor():
        address=str(doctor_entry.get())
        try: 
            contract_deployed.functions.patient_add_reader(address).transact()
            val_text=tk.Label(patient_window, text='The doctor is add!', fg='green')
            val_text.grid(row=7, column=0, sticky='WE', padx=100, pady=10)
        except: 
            val_text=tk.Label(patient_window, text='The doctor is not add. Insert a valid address!', fg='red')
            val_text.grid(row=7, column=0, sticky='WE', padx=100, pady=10)

    def remove_doctor():
        address=str(doctor_entry.get())
        try: 
            contract_deployed.functions.patient_remove_reader(address).transact()
            val_text=tk.Label(patient_window,text='The doctor is removed!', fg='green')
            val_text.grid(row=7, column=2, sticky='WE', padx=100, pady=10)
        except:
            val_text=tk.Label(patient_window,text='The doctor is not remove. Insert a valid address!', fg='red')
            val_text.grid(row=7, column=2, sticky='WE', padx=100, pady=10)   
    
    def purchase_prescription():
        val_purchase = purchase_input.get().split(',')
        id_ = int(val_purchase[0])
        quantity_ = int(val_purchase[1])
        contract_deployed.functions.patient_purchasing(id_, quantity_).call()
        validate_purchase=contract_deployed.functions.patient_purchasing(id_, quantity_).transact()
        print(validate_purchase)
    
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
    purchase_input=tk.Entry(patient_window, justify=tk.CENTER, textvariable=v, 
                            fg = 'gray78', font = 'italic')
    purchase_input.grid(row=2, column=1, sticky='WE', padx=100, pady=10)

    purchase_button=tk.Button(patient_window, text='Purchase!', command=purchase_prescription,
                              fg="blue4", bg ='orange', bd=4, font="arial 18")
    purchase_button.grid(row=3, column=1, sticky='WE', padx=10, pady=10)

    # My prescriptions
    my_prescr = tk.Button(patient_window, text='My Prescriptions', command = patient_prescriptions,
                          fg="blue4", bg ='orange', bd=4, font="arial 15")
    my_prescr.grid(row=3, column=0, sticky='WE', padx=10, pady=10)

    # Details prescription
    id_presc = tk.StringVar(patient_window, value='id_prescription')
    prescr_details=tk.Entry(patient_window, justify=tk.CENTER, textvariable=id_presc, 
                                  fg = 'gray78')
    prescr_details.grid(row=2, column=2, sticky='WE', padx=100, pady=10)
    button_details=tk.Button(patient_window, text='Details', command = prescription_details,
                             fg="blue4", bg ='orange', bd=4, font="arial 15")
    button_details.grid(row=3, column=2, sticky='WE', padx=10, pady=10)
    
    # Doctors section
    tkinter.ttk.Separator(patient_window, orient='horizontal').grid(column=0,
        row=5, sticky='WE',padx=10, pady=10,columnspan=3)
    doct_section = tk.Label(patient_window, text='Manage doctor access', font = 30, bg ='orange')
    doct_section.grid(row=5, column=1,sticky='WE', padx=100, pady=10) 
    # tkinter.ttk.Separator(patient_window, orient='horizontal').grid(column=2,
    #     row=7, sticky='WE', padx=10, pady=10)   

    id_doct = tk.StringVar(patient_window, value='Doctor public id')
    doctor_entry=tk.Entry(patient_window, justify=tk.CENTER, textvariable=id_doct, 
                              fg = 'gray78', font = 'italic')
    doctor_entry.grid(row=6, column=1, sticky='WE', padx=100, pady=10)

    # Add Doctor
    add_button=tk.Button(patient_window, text='Add Doctor', command = add_doctor,
                         fg="blue4", bg ='orange', bd=4, font="arial 15")
    add_button.grid(row=6, column=0, sticky='WE', padx=100, pady=10)

    # Remove Doctor
    add_button=tk.Button(patient_window, text='Remove Doctor', command = remove_doctor,
                         fg="blue4", bg ='orange', bd=4, font="arial 15")
    add_button.grid(row=6, column=2, sticky='WE', padx=100, pady=10)
    
def pharma_window_():
    def sell_drug():
        _id=int(prescID.get())
        quantity=int(quantity_input.get())
        contract_deployed.functions.close_transaction(_id,quantity).transact()
    
    def patient_prescriptions():
        address=str(patient_address_input2.get())
        details=patient_prescriptions_global(address)
        print(details)
    
    def prescription_details():
        _id=int(prescrId_input.get())
        details=prescription_details_global(_id)
        print(details)
        
    pharma_window=tk.Toplevel()
    pharma_window.geometry('1200x600')
    pharma_window.title('Pharma interface')
    for col in range(3):
        pharma_window.grid_columnconfigure(col, weight=1)
    for row in range(7):
        pharma_window.grid_rowconfigure(row, weight=1)
        
    title_doctor=tk.Label(pharma_window, text='Hello Pharmacy!', font=(30))
    title_doctor.grid(row=0,column=1,sticky='N', padx=10,pady=10)
    
    subtitle_doctor=tk.Label(pharma_window, text='Here you can sell your drugs')
    subtitle_doctor.grid(row=1,column=1,sticky='WE', padx=10,pady=10)
    
    first_section=tk.Label(pharma_window, text='Confirm prescription')
    first_section.grid(row=2,column=1,sticky='WE', padx=10,pady=10)
    
    prescID=tk.Entry(pharma_window,justify=tk.CENTER, textvariable=tk.StringVar(pharma_window,'id_prescription'), 
                            fg = 'gray78', font = 'italic')
    prescID.grid(row=3, column=0, sticky='WE', padx=100, pady=10)
    
    quantity_input=tk.Entry(pharma_window,justify=tk.CENTER, textvariable=tk.StringVar(pharma_window,'quantity'), 
                            fg = 'gray78', font = 'italic')
    quantity_input.grid(row=3, column=1, sticky='WE', padx=100, pady=10)
    
    close_transaction_button=tk.Button(pharma_window, text='Confirm prescription',
                                                 command = sell_drug)
    close_transaction_button.grid(row=3,column=2,sticky='WE', padx=100,pady=10) 
    
    tkinter.ttk.Separator(pharma_window, orient='horizontal').grid(column=0,
    row=4, sticky='WE',padx=10, pady=10,columnspan=3)
    
    second_section=tk.Label(pharma_window, text='Manage Prescriptions')
    second_section.grid(row=5,column=1,sticky='WE', padx=10,pady=10)
    
    patient_address_input2=tk.Entry(pharma_window,justify=tk.CENTER, textvariable=tk.StringVar(pharma_window,'patient_address'), 
                            fg = 'gray78', font = 'italic')
    patient_address_input2.grid(row=6, column=0, sticky='WE', padx=100, pady=10)
    
    check_patient_prescriptions_button=tk.Button(pharma_window, text='Check patient prescriptions',
                                                 command = patient_prescriptions)
    check_patient_prescriptions_button.grid(row=6,column=1,sticky='WE', padx=40,pady=10)
     
    prescrId_input=tk.Entry(pharma_window,justify=tk.CENTER, textvariable=tk.StringVar(pharma_window,'prescription_ID'), 
                            fg = 'gray78', font = 'italic')
    prescrId_input.grid(row=7, column=0, sticky='WE', padx=100, pady=10)
    
    prescription_details_button=tk.Button(pharma_window, text='Check prescriptions details',
                                                 command = prescription_details)
    prescription_details_button.grid(row=7,column=1,sticky='WE', padx=40,pady=10) 

def bitpharma_window_():
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

global id_entry
id_entry=tk.Entry(master, justify=tk.CENTER, show="*")
id_entry.grid(row=3,column=0,sticky='WE', padx=100, pady=10)

first_button=tk.Button(master,text='Access as doctor', command = doctor_login,
                       bg ='sky blue', fg="dark green", bd=4, font="arial 15")
first_button.grid(row=4,column=0,sticky='WE',padx=100, pady=10,)

second_button=tk.Button(master, text='Access as patient',command = patient_login,
                        bg ='sky blue', fg="dark green", bd=4, font="arial 15")
second_button.grid(row=5,column=0,sticky='WE',padx=100,pady=10)

third_button=tk.Button(master, text='Access as pharma',command = pharma_login,
                       bg ='sky blue', fg="dark green", bd=4, font="arial 15")
third_button.grid(row=6,column=0,sticky='WE',padx=100, pady=10)

fourth_button=tk.Button(master, text='Access as BitPharma Manger', command = bitpharma_login,
                        bg ='sky blue', fg="dark green", bd=4, font="arial 15")
fourth_button.grid(row=7,column=0,sticky='WE',padx=100,pady=10)

if __name__=='__main__':
    master.mainloop()
