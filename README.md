# BitPharma - Medical Prescriptions on Ethereum

In Italy, a lot of medical prescriptions are still hand written: electronic prescription are only required when the drug is paid by the regional public system, but every pharmaceutical drug that legally requires a medical prescription can still be bought with a hand-written prescription. This leads to an **authenticity problem**. Moreover, it is common practice that a pharmacist does not ask for a medical prescription, even if it is needed. These behaviors could pose a serious risk of **drug use disorders** and **overmedication** among the population. This project aims to try and provide a solution to these issues. 

Our service consists of a **blockchain application**, that authenticates medical prescriptions and facilitates exchange of information between medical doctors, pharmacies and authorities, creating an aggregate prescriptions database in a secure way.

Prescriptions that are transmitted using the blockchain platform can be verified together with the identities of the medical doctor and the patient. Pharmacists would then be able to confirm the authenticity of the prescription, to ensure that they are selling a medicine for legitimate use. 

Blockchain would also overcome the issue of **privacy** for health data, as patient's information would be de-identified, so that only trusted readers, selected by the patient, can associate the patient with the records present in the blockchain.

## Overview - how it works

Doctors, patients and pharmacies can **register** on Bitpharma by entering their information, e.g. their Social Security number. Once registered, doctors can **prescribe** medicines to patients with various indications, such as the max quantity claimable in a single purchase or the expiration date. 
When the patient wants to purchase the medicine, he/she can send a **purchase request**, and once it has been submitted, the pharmacy can **close** the prescription and sell the medicine to the patient. 

Throughout the entire process, the patients' **privacy** is protected. Indeed, they are the only ones who can grant someone access to their information and their list of prescriptions, and can revoke this at any time. 

The **roles** defined in the project are the following:

 1. **Doctor**: the doctor can prescribe medications to the patients by executing a smart contract that generates the prescription based on various metadata - *such as  patient address, quantity and expiration date.* If the patient allows it, a doctor can also have access to his/her historical record of prescribed drugs. Either way, when the medicine is prescribed, if there is already an active prescription (i.e. not expired and not fully exhausted) for the same drug, the physician is notified and cannot generate the prescription. This prevents a patient from having multiple doctors prescribe the same drug. 

2. **Patient**: when the doctor prescribes a drug to the patient, he/she can purchase it, by sending a purchase request to the pharmacy. 
3. **Pharmacy**: Authenticated pharmacies can disburse the drug after the patient's purchase request has gone through. Once they have checked the prescription ID and the quantity requested by the patient, they can sell the drug and close the transaction. 

## Contracts

This process is enabled by two contracts: 

- **whitelist** 
- **prescriptions**

#### Whitelist
The ***whitelist*** contract is used to manage users - *doctors, patients, pharmacies* - registered on BitPharma via mappings (address, bool). In particular, only the BitPharma manager can add or remove users, and these mappings will be used in the core contract - *prescriptions* - to verify the addresses. In this way, we can ensure that prescriptions are filled by a registered physician, directed towards addresses corresponding to valid patients, and drugs are only sold by a certified pharmacy.

#### Prescriptions

Let us now investigate our main contract and its functionalities. 

**Prescriptions** are embodied in the stuct *prescriptions*. In particular, we have taken into account the possibility of issuing repeatable prescriptions, i.e. prescriptions that allow the same prescription to be dispensed more than once. For this reason we added some variables such as the purchase_cooldown to allow the doctor to set a time before which the patient cannot re-purchase the medicine; e.g. one pack per month for a 6 months period. 

Specifically, the struct **prescription** is characterized by the following attributes: 

 1. *drug*: name of the drug to be prescribed
 2. *quantity*: total quantity of the drug claimable before the prescription expires
 3. *quantity_claimed*: quantity claimed by user in a single purchase 
 4. *maxclaim*: max amount claimable in single purchase. E.g. the doctor can set a limit to 1 package of the drug each purchase.
 5. *purchase_cooldown*: number of days for the patient to be able to buy the drug again. 
 6. *last_purchase*: timestamp of latest purchase
 7. *expiration*: days from when prescription was issued
 8. *status*: it can take value from 0 to 3 based on the status of the prescription. In particular,  0 means that the prescription has been issued. It takes value 1 once the patient has confirmed the purchase and 2 when the pharmacy has closed the transaction successfully. Finally, if the prescription expires before being used, the status takes value 3.
 9. *doctor*: doctor who issued the prescription
 
 At a more developed stage, most of these attributes would be constrained to values that comply with current regulation. For instance, Italian laws allow for prescriptions of up to two packages for most drugs, which increases to three for drugs used to treat chronic diseases and to six for injectable antibiotics. This could be achieved by allowing the contract to communicate with an external database that would contain all of these requirements, and then add checks in the code to ensure full compliance to the regulation.

We used internal `mappings` to connect:
1. each prescription ID to the patient address;
2. drug hashes of active prescriptions to each patient;
3. each prescription ID to the pharmacy who closed it and to the quantity;
4. prescription IDs to the array of the pharmacy who closed it
5. A mapping of mapping is used for the addresses who can access patient information. These addresses are called *readers*: they are authorized by the patient to read all of their prescriptions (they are usually doctors, but can also be family members etc.). The patient is the only one who can add or remove readers, through the `patient_remove_reader` and `patient_add_reader` functions, in this way his privacy will be protected.
`set_whitelist_address`: this function can only be used by the bitpharma mananger and it is necessary to link the *core contract* to the *whitelist* one. In this way the address of a pharmacy/physician/patient will be linked to the one registered in the whitelist. 

`new_prescription`: with this function, a whitelisted doctor can issue a new prescription to a valid patient address. Authentication is achieved through require functions that ascertains that the address is a registered doctor/patient, by verifying the whitelist contract. The function takes as inputs the drug name, its quantity, max claim, purchase cooldown, days to expiration and patient's address. In particular, to make sure the prescription is not issued with an expiration date greater than three months, we have included a require function. The same was done to be assured that the expiration date is not less than the purchase cooldown, multiplied by the quantity, divided by the max claim. If it were the case, the patient would not be able to purchase the prescribed amount of medicine by the expiration date. Finally, the `check_active_prescriptions`function checks whether the patient already has an active prescription for the same drug. 
By calling this function, patient's information is updated, adding the prescription to the *patient_active_prescriptions* array. 


