# BitPharma - Medical Prescriptions on Ethereum

In Italy, a lot of medical prescriptions are still hand written: electronic prescription are only required when the drug is paid by the regional public system, but every pharmaceutical drug that legally requires a medical prescription can still be bought with a hand-written prescription. This leads to an **authenticity problem**. Moreover, it is common practice that a pharmacist does not ask for a medical prescription, even if it is needed. These behaviors could pose a serious risk of **drug use disorders** and **overmedication** among the population. This project aims to try and provide a solution to these issues. 

Our service consists of a **blockchain application**, that authenticates medical prescriptions and facilitates exchange of information between medical doctors, pharmacies and authorities, creating an aggregate prescriptions database in a secure way. Prescriptions that are transmitted using the blockchain platform can be verified together with the identities of the medical doctor and the patient. Pharmacists would then be able to confirm the authenticity of the prescription, to ensure that they are selling a medicine for legitimate use. 

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

### Whitelist
The ***whitelist*** contract is used to manage users - *doctors, patients, pharmacies* - registered on BitPharma via mappings (address, bool). In particular, only the BitPharma manager can add or remove users, and these mappings will be used in the core contract - *prescriptions* - to verify the addresses. In this way, we can ensure that prescriptions are filled by a registered physician, directed towards addresses corresponding to valid patients, and drugs are only sold by a certified pharmacy.

### Prescriptions

Let us now investigate our main contract and its functionalities. 

**Prescriptions** are embodied in the stuct *prescriptions*. In particular, we have taken into account the possibility of issuing repeatable prescriptions, i.e. prescriptions that allow the same prescription to be dispensed more than once. For this reason we added some variables such as the purchase_cooldown to allow the doctor to set a time before which the patient cannot re-purchase the medicine; e.g. one pack per month for a 6 months period. 

Specifically, the struct `prescription` is characterized by the following attributes: 

 1. *drug*: name of the drug to be prescribed
 2. *quantity*: total quantity of the drug claimable before the prescription expires
 3. *quantity_claimed*: quantity claimed by user in a single purchase 
 4. *maxclaim*: max amount claimable in single purchase. E.g. the doctor can set a limit to 1 package of the drug each purchase.
 5. *purchase_cooldown*: number of days for the patient to be able to buy the drug again. 
 6. *last_purchase*: timestamp of latest purchase
 7. *expiration*: days from when prescription was issued
 8. *status*: it can take value from 0 to 3 based on the status of the prescription. In particular,  0 means that the prescription has been issued. It takes value 1 once the patient has confirmed the purchase and 2 when the pharmacy has closed the transaction successfully. Finally, if the prescription expires before being used, the status takes value 3.
 9. *doctor*: doctor who issued the prescription
 
We keep track of all prescriptions being issued in the chain with the array `prescriptions`. Given a presription id, the only users that can view the details of that prescription are the recipient of it, external users allowed by the recipient ("readers"), the doctor who issued it and the pharmacies at point of sale. Note that, when viewing the details of a prescription with a call to `prescription_details` there is no reference to the addresses of the patient and the doctor (checks are carried out internally when selling or requesting access), as a further privacy guarantee.
 
 At a more developed stage, most of these attributes would be constrained to values that comply with current regulation. For instance, Italian laws allow for prescriptions of up to two packages for most drugs, which increases to three for drugs used to treat chronic diseases and to six for injectable antibiotics. This could be achieved by allowing the contract to communicate with an external database that would contain all of these requirements, and then add checks in the code to ensure full compliance to the regulation.
 
We used several internal `mappings`, to allow for easy information retrieval and to enable the use of different require() statements in function calls.
In particual, we mapped:
1. `prescription_to_patient`: each prescription ID to the corresponding patient address;
2. `patient_readers`: for each patient address, the addresses of the other users who have been explicitly allowed access to their prescription history (e.g. their doctor). Patient can add and remove new readers with a call to the `patient_add_reader` and `patient_remove_reader` functions. Only allowed readers can access the prescription history of a patient.  
3. `patient_active_prescriptions`: a nested mapping; for each patient address, and each drug, map to a boolean that indicates whether or not they have an active prescription for the drug. This is necessary, as we see below, to check and avoid co-occurring double prescriptions.
4. `patient_id_prescriptions`: for each patient, a list of prescriptions ids that make up his/her whole prescription history.
5. `patient_drug_expiration`: a nested mapping; for each patient, and each prescribed drug, map to the expiration of the corresponding prescription
6. `patient_drug_id`: a nested mapping;  for each patient, and prescribed drug, map to the id of the corresponding active prescription
7. `prescription_to_pharmacy_quantity`: a nested mapping; for each prescription id, map to the pharmacy who closed it and the quantity sold. 
8. `prescription_to_pharmacy`: for each prescription id, map to the address of the pharmacy who closed it.
9. `is_old_patient`: for each patient address, map to a boolean stating whether the pateint is a new user (i.e. there has never been a prescription made towards him/her on the blockchain).

Mappings 7 and 8 are drafts, meant to allow for easier checks by special categories of readers such as law enforcements, via the `get_prescription_pharmacies` and `get_prescription_pharmacy_quantity`functions which are at this stage simple external view function. More on this in the caveats.

#### Main functions

`new_prescription`: with this function, a whitelisted doctor can issue a new prescription to a valid patient address. Authentication is achieved through require functions that ascertain that the addresses belong to a pair of registered doctor/patient, by verifying with the whitelist contract. The function takes as inputs the drug name, its quantity, maximum claimable amount, purchase cooldown period, days to expiration of the prescription and the patient's address. In particular, to make sure the prescription is not issued with an expiration date greater than three months, we have included a require function. The same was done to ensure that the expiration date is not less than the purchase cooldown, multiplied by the quantity, divided by the maximum claimable amount. If it were the case, the patient would not be able to purchase the prescribed amount of medicine by the expiration date. Finally, the `check_active_prescriptions`function checks whether the patient already has an active prescription for the same drug. If that is the case, the transaction cannot go through. 
By calling the new_prescription function, the patient's information is also updated, adding the new prescription to the *patient_active_prescriptions* array and cleaning it from expired ones (which get status changed to 3) if there are any. The status of a new prescription is initialised as 0.

`patient_purchasing`: through the prescription_id, the patient can launch the request to purchase the medicine. There are several require functions to check that the patient is actually the holder of that prescription, that the prescription is not expired and that the quantity requested does not exceed the quantity prescribed; also, the function makes sure that the patient is respecting the purchase cooldown period in case he/she has made a previous purchase with the same prescription id. If the transaction is successful, the prescription status is updated to 1. 

`close_transaction`: once the prescription status is equal to 1 (i.e. the patient has requested to make a purchase), the pharmacy can proceed with the sale. This function will close the transaction and certify the sale of the medicine to the patient. If there is no outstanding claimable quantity in the prescription after the purchase , then the prescription is finally closed with status 2. Otherwise, the available quantity is reduced by the quantity purchased and the prescription status is changed back to 0. In this way, the prescription will still be available to the patient to purchase the remaining prescribed quantity. This function can only be called by a registered pharmacy and the authentication is achieved by verifying the address against the whitelist contract.

