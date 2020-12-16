import tkinter as tk
from PIL import ImageTk, Image
import json
from web3 import Web3
import tkinter.ttk

with open('./contract_data/bitpharma.abi') as json_file:
    abi_ = json.loads(json_file.read())

with open('./Interface/contract_data/bitpharma.bin') as file:
    bin_ = file.read()

with open('./contract_data/bitpharma_wl.abi') as json_file:
    abi_wl = json.loads(json_file.read())

with open('./contract_data/bitpharma_wl.bin') as file:
    bin_wl = file.read()

ganache_URL = "HTTP://127.0.0.1:7545"
w3 = Web3(Web3.HTTPProvider(ganache_URL))

master=tk.Tk()
master.geometry('900x900')
master.title('Medical prescription Ethereum')

# Bitpharma login must be the first one, cannot acces other contracts
def bitpharma_login():
    bitpharma_manager=str(id_entry.get())
    w3.eth.defaultAccount = bitpharma_manager
    bitpharma_window_()

def patient_login():
    try:
        contract_deployed
        patient_account=str(id_entry.get())
        w3.eth.defaultAccount = patient_account
        access = contract_deployed_.functions.patients(patient_account).call()
        if access:
            patient_window_()
        else:
            subtitle=tk.Label(master, text='You are not registered as patient!',
                            bg ='sky blue', fg = 'red')
            subtitle.grid(row=2,column=0,sticky='WE', padx=100, pady=1)
    except NameError:
        subtitle=tk.Label(master, text='Contract not deployed by BitPharma',
                          bg ='sky blue', fg = 'red')
        subtitle.grid(row=2,column=0,sticky='WE', padx=100, pady=1)

def doctor_login():
    try:
        contract_deployed
        doc_account=str(id_entry.get())
        w3.eth.defaultAccount = doc_account
        access = contract_deployed_.functions.doctors(doc_account).call()        
        if access:
            doctor_window_()
        else:
            subtitle=tk.Label(master, text='You are not registered as doctor!',
                          bg ='sky blue', fg = 'red')
            subtitle.grid(row=2,column=0,sticky='WE', padx=100, pady=1)
    except NameError:
        subtitle=tk.Label(master, text='Contract not deployed by BitPharma',
                          bg ='sky blue', fg = 'red')
        subtitle.grid(row=2,column=0,sticky='WE', padx=100, pady=1)

def pharma_login():
    try:
        contract_deployed
        pharma_account=str(id_entry.get())
        w3.eth.defaultAccount = pharma_account
        access = contract_deployed_.functions.pharmacies(pharma_account).call()        
        if access:
            pharma_window_()
        else:
            subtitle=tk.Label(master, text='You are not registered as pharma!',
                          bg ='sky blue', fg = 'red')
            subtitle.grid(row=2,column=0,sticky='WE', padx=100, pady=1)
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
        try:
            contract_deployed.functions.new_prescription(drug,quantity,maxclaim,purchaseCooldown,daysToExpiration,patient).transact()
            descr=tk.Label(doctor_window, text="Prescribed!", font=10, fg='green')
            descr.grid(row=5,column=2,sticky='WE', padx=100,pady=10)
        except:
            descr=tk.Label(doctor_window, text="There is a mistake \nin the prescription!", font=10, fg ='red')
            descr.grid(row=5,column=2,sticky='WE', padx=100,pady=10)

    def patient_prescriptions():
        address=str(patient_address_input2.get())
        try:
            details=patient_prescriptions_global(address)
            descr=tk.Label(doctor_window, text=details, font=10)
            descr.grid(row=8,column=2,sticky='WE', padx=100,pady=10)
        except:
            descr=tk.Label(doctor_window, text="You can't see the \npatient prescritpions", font=10, fg ='red')
            descr.grid(row=8,column=2,sticky='WE', padx=100,pady=10)
        
    def prescription_details():
        _id=int(prescrId_input.get())
        try:
            details=prescription_details_global(_id)
            drugname = details[0]
            quantity = details[1]
            max_claim = details[2]
            can_buy = details[3]
            expire_in = details[4]
            status = details[5]
            to_print = f'''drug: {drugname}\nquantity: {quantity}\nmax_claim: {max_claim}\ncan_buy: {can_buy}\nexpire_in: {expire_in} days\nstatus: {status}'''
            descr=tk.Label(doctor_window, text=to_print, font=10)
            descr.grid(row=9,column=2,sticky='WE', padx=100,pady=10)
        except:
            descr=tk.Label(doctor_window, text="You can't see the details \nof this prescritpion", font=10)
            descr.grid(row=9,column=2,sticky='WE', padx=100,pady=10)

    doctor_window=tk.Toplevel()
    doctor_window.geometry('1200x700')
    doctor_window.title('Doctor interface')

    # Background
    back_image = Image.open('./images/background_doctor.png')
    back_image = back_image.resize((1800,1500))
    background_image = ImageTk.PhotoImage(back_image)
    background_label = tk.Label(doctor_window, image=background_image)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)
    background_label.image = background_image

    for col in range(3):
        doctor_window.grid_columnconfigure(col, weight=1)
    for row in range(10):
        doctor_window.grid_rowconfigure(row, weight=1)

    #title_doctor=tk.Label(doctor_window, text='Hello doctor!', font=(30))
    #title_doctor=tk.Label(doctor_window, text='', font=(30))
    #title_doctor.grid(row=0,column=1,sticky='N', padx=10,pady=10)

    subtitle_doctor=tk.Label(doctor_window, text='Here you can prescribe to your patients \nand check their prescriptions',
                             fg="blue4", bd=4, font="arial 15")
    subtitle_doctor.grid(row=1,column=1,sticky='WE', padx=10,pady=10)

    first_section=tk.Label(doctor_window, text='New Prescription', fg="blue4", bd=4, font="arial 15")
    first_section.grid(row=2,column=1,sticky='WE', padx=10,pady=10)

    drug_input=tk.Entry(doctor_window,justify=tk.CENTER, textvariable=tk.StringVar(doctor_window,'drug'),
                            fg = 'gray78', font = 'italic', bd=4)
    drug_input.grid(row=3, column=0, sticky='WE', padx=100, pady=10)

    quantity_input=tk.Entry(doctor_window,justify=tk.CENTER, textvariable=tk.StringVar(doctor_window,'quantity'),
                            fg = 'gray78', font = 'italic', bd=4)
    quantity_input.grid(row=3, column=1, sticky='WE', padx=100, pady=10)

    maxclaim_input=tk.Entry(doctor_window,justify=tk.CENTER, textvariable=tk.StringVar(doctor_window,'maxclaim'),
                            fg = 'gray78', font = 'italic', bd=4)
    maxclaim_input.grid(row=3, column=2, sticky='WE', padx=100, pady=10)

    purchaseCooldown_input=tk.Entry(doctor_window,justify=tk.CENTER, textvariable=tk.StringVar(doctor_window,'purchaseCooldown'),
                            fg = 'gray78', font = 'italic', bd=4)
    purchaseCooldown_input.grid(row=4, column=0, sticky='WE', padx=100, pady=10)

    daysToExpiration_input=tk.Entry(doctor_window,justify=tk.CENTER, textvariable=tk.StringVar(doctor_window,'daysToExpiration'),
                            fg = 'gray78', font = 'italic', bd=4)
    daysToExpiration_input.grid(row=4, column=1, sticky='WE', padx=100, pady=10)

    patient_address_input=tk.Entry(doctor_window,justify=tk.CENTER, textvariable=tk.StringVar(doctor_window,'patient_address'),
                            fg = 'gray78', font = 'italic', bd=4)
    patient_address_input.grid(row=4, column=2, sticky='WE', padx=100, pady=10)

    prescribe_button=tk.Button(doctor_window, text='Prescribe',command = prescribe_drug,
                               fg="blue4", bd=4, font="arial 15")
    prescribe_button.grid(row=5,column=1,sticky='WE', padx=150,pady=10)

    tkinter.ttk.Separator(doctor_window, orient='horizontal').grid(column=0,
    row=6, sticky='WE',padx=10, pady=10,columnspan=3)

    second_section=tk.Label(doctor_window, text='Manage Prescriptions',
                            fg="blue4", bd=4, font="arial 15")
    second_section.grid(row=7,column=1,sticky='WE', padx=10,pady=10)

    patient_address_input2=tk.Entry(doctor_window,justify=tk.CENTER, textvariable=tk.StringVar(doctor_window,'patient_address'),
                            fg = 'gray78', font = 'italic', bd=4)
    patient_address_input2.grid(row=8, column=0, sticky='WE', padx=100, pady=10)

    check_patient_prescriptions_button=tk.Button(doctor_window, text='Check patient prescriptions',
                                                 command = patient_prescriptions, fg="blue4", bd=4, font="arial 15")
    check_patient_prescriptions_button.grid(row=8,column=1,sticky='WE', padx=40,pady=10)

    prescrId_input=tk.Entry(doctor_window,justify=tk.CENTER, textvariable=tk.StringVar(doctor_window,'prescription_ID'),
                            fg = 'gray78', font = 'italic', bd=4)
    prescrId_input.grid(row=9, column=0, sticky='WE', padx=100, pady=10)

    prescription_details_button=tk.Button(doctor_window, text='Check prescriptions details',
                                          command = prescription_details, fg="blue4", bd=4, font="arial 15")
    prescription_details_button.grid(row=9,column=1,sticky='WE', padx=40,pady=10)


def patient_window_():
    def patient_prescriptions():
        address=str(id_entry.get())
        try:
            details=patient_prescriptions_global(address)
            descr=tk.Label(patient_window, text=details, font=10)
            descr.grid(row=4,column=0,sticky='WE', padx=100,pady=10)
        except:
            pass

    def prescription_details():
        _id=int(prescr_details.get())
        try:
            details=prescription_details_global(_id)
            drugname = details[0]
            quantity = details[1]
            max_claim = details[2]
            can_buy = details[3]
            expire_in = details[4]
            status = details[5]
            to_print = f'''drug: {drugname}\nquantity: {quantity}\nmax_claim: {max_claim}\ncan_buy: {can_buy}\nexpire_in: {expire_in} days\nstatus: {status}'''
            descr=tk.Label(patient_window, text=to_print, font=10)
            descr.grid(row=4,column=2,sticky='WE', padx=100,pady=10)
        except:
            descr=tk.Label(patient_window, text="You can't see the details of this prescritpion", font=10)
            descr.grid(row=4,column=2,sticky='WE', padx=100,pady=10)

    def add_doctor():
        address=str(doctor_entry.get())
        try:
            contract_deployed.functions.patient_add_reader(address).transact()
            val_text=tk.Label(patient_window, text='The doctor has been added!', fg='green')
            val_text.grid(row=7, column=0, sticky='WE', padx=100, pady=10)
        except:
            val_text=tk.Label(patient_window, text='The doctor has not been added. Insert a valid address!', fg='red')
            val_text.grid(row=7, column=0, sticky='WE', padx=100, pady=10)

    def remove_doctor():
        address=str(doctor_entry.get())
        try:
            contract_deployed.functions.patient_remove_reader(address).transact()
            val_text=tk.Label(patient_window,text='The doctor has been removed!', fg='green')
            val_text.grid(row=7, column=2, sticky='WE', padx=100, pady=10)
        except:
            val_text=tk.Label(patient_window,text='The doctor has not been remove. Insert a valid address!', fg='red')
            val_text.grid(row=7, column=2, sticky='WE', padx=100, pady=10)

    def purchase_prescription():
        val_purchase = purchase_input.get().split(',')
        id_ = int(val_purchase[0])
        quantity_ = int(val_purchase[1])
        contract_deployed.functions.patient_purchasing(id_, quantity_).transact()
        descr=tk.Label(patient_window, text='Validated!', font=10)
        descr.grid(row=4,column=1,sticky='WE', padx=100, pady=10)
    
    patient_window=tk.Toplevel()
    patient_window.geometry('1200x1500')
    patient_window.title('Patient interface')

    # Background
    back_image = Image.open('./images/background_patient.png')
    back_image = back_image.resize((1800,1500))
    background_image = ImageTk.PhotoImage(back_image)
    background_label = tk.Label(patient_window, image=background_image)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)
    background_label.image = background_image

    for col in range(3):
        patient_window.grid_columnconfigure(col, weight=1)
    for row in range(9):
        patient_window.grid_rowconfigure(row, weight=1)

    #title=tk.Label(patient_window, text='Hello patient', font=30,  bg ='orange')
    #title.grid(row=0, column=1, sticky='WE', padx=100, pady=10)
    title=tk.Label(patient_window, text='Here you can buy your medicine:', font=30,  bg ='orange')
    title.grid(row=1, column=1, sticky='WE', padx=100, pady=5)

    # Purchase
    v = tk.StringVar(patient_window, value='id_prescription, quantity')
    purchase_input=tk.Entry(patient_window, justify=tk.CENTER, textvariable=v,
                            fg = 'gray78', font = 'italic', bd=4)
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
                                  fg = 'gray78', bd=4)
    prescr_details.grid(row=2, column=2, sticky='WE', padx=100, pady=10)
    button_details=tk.Button(patient_window, text='Details', command = prescription_details,
                             fg="blue4", bg ='orange', bd=4, font="arial 15")
    button_details.grid(row=3, column=2, sticky='WE', padx=10, pady=10)

    # Doctors section
    tkinter.ttk.Separator(patient_window, orient='horizontal').grid(column=0,
        row=5, sticky='WE',padx=10, pady=10,columnspan=3)
    doct_section = tk.Label(patient_window, text='Manage doctor access', font = 30, bg ='orange')
    doct_section.grid(row=5, column=1,sticky='WE', padx=100, pady=10)

    id_doct = tk.StringVar(patient_window, value='Doctor public id')
    doctor_entry=tk.Entry(patient_window, justify=tk.CENTER, textvariable=id_doct,
                              fg = 'gray78', font = 'italic', bd=4,)
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
        try:
            quantity=int(quantity_input.get())
            contract_deployed.functions.close_transaction(_id,quantity).transact()
            descr=tk.Label(pharma_window, text="Drug sold!", fg="blue4", bd=4, font="arial 15")
            descr.grid(row=4,column=2,sticky='WE', padx=100,pady=10)
        except: 
            descr=tk.Label(pharma_window, text="Drug not sold!", fg="red", bd=4, font="arial 15")
            descr.grid(row=4,column=2,sticky='WE', padx=100,pady=10)

    def patient_prescriptions():
        address=str(patient_address_input2.get())
        try:
            details=patient_prescriptions_global(address)
            descr=tk.Label(pharma_window, text=details, fg="blue4", bd=4, font="arial 15")
            descr.grid(row=6,column=2,sticky='WE', padx=100,pady=10)
        except:
            descr=tk.Label(pharma_window, text="You can't see the \npatient prescritpions", fg="red", bd=4, font="arial 15")
            descr.grid(row=6,column=2,sticky='WE', padx=100,pady=10)

    def prescription_details():
        _id=int(prescrId_input.get())
        try:
            details=prescription_details_global(_id)
            drugname = details[0]
            quantity = details[1]
            max_claim = details[2]
            can_buy = details[3]
            expire_in = details[4]
            status = details[5]
            to_print = f'''drug: {drugname}\nquantity: {quantity}\nmax_claim: {max_claim}\ncan_buy: {can_buy}\nexpire_in: {expire_in} days\nstatus: {status}'''
            descr=tk.Label(pharma_window, text=to_print,  fg="blue4", bd=4, font="arial 13")
            descr.grid(row=7,column=2,sticky='WE', padx=100,pady=10)
        except:
            descr=tk.Label(pharma_window, text="You can't see the details \nof this prescritpion", fg="red", bd=4, font="arial 15")
            descr.grid(row=7,column=2,sticky='WE', padx=100,pady=10)    

    pharma_window=tk.Toplevel()
    pharma_window.geometry('1300x700')
    pharma_window.title('Pharma interface')

    # Background
    back_image = Image.open('./images/background_pharmacy.png')
    back_image = back_image.resize((1800,1500))
    background_image = ImageTk.PhotoImage(back_image)
    background_label = tk.Label(pharma_window, image=background_image)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)
    background_label.image = background_image

    for col in range(3):
        pharma_window.grid_columnconfigure(col, weight=1)
    for row in range(7):
        pharma_window.grid_rowconfigure(row, weight=1)

    #title_doctor=tk.Label(pharma_window, text='Hello Pharmacy!', font=30, fg="blue4", bd=4)
    #title_doctor.grid(row=0,column=1,sticky='N', padx=10, pady=10)

    subtitle_doctor=tk.Label(pharma_window, text='Here you can sell your drugs', fg="blue4", bd=4, font="arial 15")
    subtitle_doctor.grid(row=1,column=1,sticky='WE', padx=10, pady=10)

    first_section=tk.Label(pharma_window, text='Confirm prescription', fg="blue4", bd=4, font="arial 18")
    first_section.grid(row=2,column=1,sticky='WE', padx=10,pady=10)

    prescID=tk.Entry(pharma_window,justify=tk.CENTER, textvariable=tk.StringVar(pharma_window,'id_prescription'),
                            fg = 'gray78', font = 'italic', bd=4)
    prescID.grid(row=3, column=0, sticky='WE', padx=100, pady=10)

    quantity_input=tk.Entry(pharma_window,justify=tk.CENTER, textvariable=tk.StringVar(pharma_window,'quantity'),
                            fg = 'gray78', font = 'italic', bd=4)
    quantity_input.grid(row=3, column=1, sticky='WE', padx=100, pady=10)

    close_transaction_button=tk.Button(pharma_window, text='Confirm prescription',
                                       command = sell_drug, fg="blue4", bd=4, font="arial 15")
    close_transaction_button.grid(row=3,column=2,sticky='WE', padx=100,pady=10)

    tkinter.ttk.Separator(pharma_window, orient='horizontal').grid(column=0,
    row=5, sticky='WE',padx=10, pady=10,columnspan=3)

    second_section=tk.Label(pharma_window, text='Manage Prescriptions', fg="blue4", bd=4, font="arial 15")
    second_section.grid(row=5,column=1,sticky='WE', padx=10,pady=10)

    patient_address_input2=tk.Entry(pharma_window,justify=tk.CENTER, textvariable=tk.StringVar(pharma_window,'patient_address'),
                            fg = 'gray78', font = 'italic', bd=4)
    patient_address_input2.grid(row=6, column=0, sticky='WE', padx=100, pady=10)

    check_patient_prescriptions_button=tk.Button(pharma_window, text='Check patient prescriptions',
                                                 command = patient_prescriptions, fg="blue4", bd=4, font="arial 15")
    check_patient_prescriptions_button.grid(row=6,column=1,sticky='WE', padx=40,pady=10)

    prescrId_input=tk.Entry(pharma_window,justify=tk.CENTER, textvariable=tk.StringVar(pharma_window,'prescription_ID'),
                            fg = 'gray78', font = 'italic', bd=4)
    prescrId_input.grid(row=7, column=0, sticky='WE', padx=100, pady=10)

    prescription_details_button=tk.Button(pharma_window, text='Check prescriptions details',
                                          command = prescription_details, fg="blue4", bd=4, font="arial 15")
    prescription_details_button.grid(row=7,column=1,sticky='WE', padx=40,pady=10)

def bitpharma_window_():
    bitpharma_window=tk.Toplevel()
    bitpharma_window.geometry('1500x800')
    bitpharma_window.title('Medical prescription Ethereum')
    
    def init_whitelist():
        bitpharma_manager=str(id_entry.get())
        try:
            #Deploying bigpharma contract
            w3.eth.defaultAccount = bitpharma_manager
            contract = w3.eth.contract(bitpharma_manager, abi = abi_, bytecode = bin_)
            tx_hash=contract.constructor().transact() 
            tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
            contract_address = tx_receipt['contractAddress'] ## address of the contract
            global contract_deployed
            contract_deployed = w3.eth.contract(address = contract_address, abi = abi_)

            #Deploying whitelist contract
            w3.eth.defaultAccount = bitpharma_manager
            contract = w3.eth.contract(bitpharma_manager, abi = abi_wl, bytecode = bin_wl)
            tx_hash=contract.constructor().transact() 
            tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
            contract_address = tx_receipt['contractAddress'] 
            global contract_deployed_
            contract_deployed_ = w3.eth.contract(address = contract_address, abi = abi_wl)
            add_contract = contract_deployed_.address
            # text_v = f'Contract deployed \n Hash: {add_contract}'
            # text=tk.Label(bitpharma_window,text=text_v, fg='green')
            # text.grid(row=3, column=2, sticky='WE', padx=30, pady=10)

            #Set whitelist
            contract_deployed.functions.set_whitelist_address(add_contract).transact()
            text=tk.Label(bitpharma_window, text='Whitelist Set!', fg='green')
            text.grid(row=4, column=1, sticky='WE', padx=30, pady=10)
            subtitle=tk.Label(master, text='Contract deployed by BitPharma\n Login with your account:',
                                bg ='sky blue', fg='green')
            subtitle.grid(row=2,column=0,sticky='WE', padx=100, pady=1)
        except:
            text=tk.Label(bitpharma_window, text='Whitelist not set: insert a valid address!', fg='red')
            text.grid(row=4, column=1, sticky='WE', padx=30, pady=10)

    def add_doctor():
        address=str(doc.get())
        try:
            contract_deployed_.functions.add_doctor(address).transact()
            val_text=tk.Label(bitpharma_window,text='Doctor added!', fg='green')
            val_text.grid(row=6, column=1, sticky='WE', padx=30, pady=10)
        except:
            text=tk.Label(bitpharma_window, text='You are not the BigPharma manager',
                         fg='red')
            text.grid(row=6, column=1, sticky='WE', padx=100, pady=10)

    def add_pharma():
        address=str(pharma.get())
        try:
            contract_deployed_.functions.add_pharmacy(address).transact()
            val_text=tk.Label(bitpharma_window,text='Pharmacy added!', fg='green')
            val_text.grid(row=8, column=1, sticky='WE', padx=30, pady=10)
        except:
            text=tk.Label(bitpharma_window, text='You are not the BigPharma manager',
                         fg='red')
            text.grid(row=8, column=0, sticky='WE', padx=100, pady=10)

    def add_patient():
        address=str(patient.get())
        try:
            contract_deployed_.functions.add_patient(address).transact()
            val_text=tk.Label(bitpharma_window,text='Patient added!', fg='green')
            val_text.grid(row=10, column=1, sticky='WE', padx=30, pady=10)
        except:
            text=tk.Label(bitpharma_window, text='You are not the BigPharma manager',
                         fg='red')
            text.grid(row=10, column=0, sticky='WE', padx=100, pady=10)

    def check_doctor():
        address=str(doc.get())
        validate_doctor=contract_deployed_.functions.doctors(address).call()
        if validate_doctor:
            val_text=tk.Label(bitpharma_window,text='The doctor is registered!', fg='green')
            val_text.grid(row=6, column=1, sticky='WE', padx=30, pady=10)
        else:
            val_text=tk.Label(bitpharma_window,text='The doctor is not registered!', fg='red')
            val_text.grid(row=6, column=1, sticky='WE', padx=30, pady=10)

    def check_pharma():
        address=str(pharma.get())
        validate_pharma=contract_deployed_.functions.pharmacies(address).call()
        if validate_pharma:
            val_text=tk.Label(bitpharma_window,text='The Pharmacy is registered!', fg='green')
            val_text.grid(row=8, column=1, sticky='WE', padx=30, pady=10)
        else:
            val_text=tk.Label(bitpharma_window,text='The Pharmacy is not registered!', fg='red')
            val_text.grid(row=8, column=1, sticky='WE', padx=30, pady=10)

    def check_patient():
        address=str(patient.get())
        validate_pharma=contract_deployed_.functions.patients(address).call()
        if validate_pharma:
            val_text=tk.Label(bitpharma_window,text='The patient is registered!', fg='green')
            val_text.grid(row=10, column=1, sticky='WE', padx=30, pady=10)
        else:
            val_text=tk.Label(bitpharma_window,text='The patient is not registered!', fg='red')
            val_text.grid(row=10, column=1, sticky='WE', padx=30, pady=10)

    for column in range(3):
        bitpharma_window.grid_columnconfigure(column, weight=1)
    for row in range(11):
        bitpharma_window.grid_rowconfigure(row, weight=1)

    back_image = Image.open('./images/pharmacy.png')
    background_image = ImageTk.PhotoImage(back_image)
    background_label = tk.Label(bitpharma_window, image=background_image)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)
    background_label.image = background_image

    #title=tk.Label(bitpharma_window, text='Welcome to Medical prescription Ethereum!', font=30, fg="green")
    #title.grid(row=0,column=1,sticky='WE', padx=10, pady=(10))

    load = Image.open('./images/logo_pharma.png')
    load = load.resize((80, 80))
    photoimage = ImageTk.PhotoImage(load)
    pharma_label = tk.Label(bitpharma_window, image=photoimage)
    pharma_label.image = photoimage
    pharma_label.place(x=995, y=65)
    
    try:
        contract_deployed_
        subtitle=tk.Label(bitpharma_window, text='Contract deployed!\n you can check users here:', fg='green', font="arial 8")
        subtitle.grid(row=3, column=1, sticky='WE', padx=100)
    except:
        deploy_button=tk.Button(bitpharma_window,text='START', command=init_whitelist,
                                fg="green", bd=4, font="arial 15")
        deploy_button.grid(row=3, column=1, sticky='WE', padx=100)

    doc=tk.Entry(bitpharma_window,justify=tk.CENTER, show="*")
    doc.grid(row=5, column=0, sticky='WE', padx=100, pady=10)

    add_doctor_button=tk.Button(bitpharma_window, text='Add doctor', command=add_doctor,
                                fg="green", bd=4, font="arial 15")
    add_doctor_button.grid(row=5, column=1, sticky='WE', padx=100, pady=10)

    check_doctor_button=tk.Button(bitpharma_window, text='Check doctor', command=check_doctor,
                                fg="green", bd=4, font="arial 15")
    check_doctor_button.grid(row=5, column=2, sticky='WE', padx=100, pady=10)

    pharma=tk.Entry(bitpharma_window, justify=tk.CENTER, show="*")
    pharma.grid(row=7, column=0, sticky='WE', padx=100, pady=10)

    add_pharma_button=tk.Button(bitpharma_window, text='Add pharmacy',command=add_pharma,
                                fg="green", bd=4, font="arial 15")
    add_pharma_button.grid(row=7, column=1, sticky='WE', padx=100, pady=10)

    check_pharma_button=tk.Button(bitpharma_window, text='Check Pharmacy',command=check_pharma,
                                fg="green", bd=4, font="arial 15")
    check_pharma_button.grid(row=7, column=2, sticky='WE', padx=100, pady=(10))

    patient=tk.Entry(bitpharma_window, justify=tk.CENTER, show="*")
    patient.grid(row=9, column=0, sticky='WE', padx=100, pady=10)

    add_patient_button=tk.Button(bitpharma_window, text='Add patient',command=add_patient,
                                fg="green", bd=4, font="arial 15")
    add_patient_button.grid(row=9, column=1, sticky='WE', padx=100, pady=10)

    check_patient_button=tk.Button(bitpharma_window, text='Check patient',command=check_patient,
                                fg="green", bd=4, font="arial 15")
    check_patient_button.grid(row=9, column=2, sticky='WE', padx=100, pady=10)

master.grid_columnconfigure(0, weight=1)
for row in range(9):
    master.grid_rowconfigure(row, weight=1)

# Background
back_image = Image.open('./images/background.jpg')
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
load = Image.open('./images/logo_pharma.png')
load = load.resize((200, 200))
photoimage = ImageTk.PhotoImage(load)
canvas.create_image(100, 100, image=photoimage)

subtitle=tk.Label(master, text='Login with your key:', bg ='sky blue')
subtitle.grid(row=2,column=0,sticky='WE', padx=100, pady=1)

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
