# M.ETH - Medical (Prescriptions) on Ethereum

In Italy, a lot of medical prescriptions are still hand written: electronic prescription are only required when the drug is paid by the regional public system, but every pharmaceutical drug that legally requires a medical prescription can still be bought with a hand-written prescription. This leads to an **authenticity problem**. Moreover, it is common practice that a pharmacist does not ask for medical prescription, even if it is needed. These behaviors cause a serious problem of **drug use disorders** among the population. This project has the aim of overcoming these kind of issues. 

This service consists in a **blockchain application** that authenticates medical prescriptions and facilitates the interoperability between medical doctors, pharmacies and authorities, creating an aggregate prescription-drugs-database in a secure way.

Prescriptions that are transmitted using the blockchain platform can be verified together with the identities of the medical doctor and the patient. Pharmacists would then be able to verify the authenticity of the prescription to ensure that they are selling a medicine for legitimate use. 

Blockchain would also overcome the issue of **privacy** for health data, as patient's information would be de-identified, so that only trusted viewers, selected by the patient, can associate the patient with the records present in the blockchain.

## Overview - how it works

Doctors, patients and pharmacies can **register** on M.ETH by entering their information, e.g. their Social Security number.  Once registered, doctors can **prescribe** medicines to patients with various indications, such as the max amount of packages claimable in a single purchase. 
When the patient wants to purchase the medicine, he/she can send a **purchase request**, and once it has been submitted, the pharmacy can **close** the prescription and sell the medicine to the patient. 

Throughout the entire process, patients' **privacy** is protected. Indeed, they will be the only ones who can decide who has access to their information and their list of prescriptions.

The **roles** defined in the project are the following:

 1. **Doctor**: the doctor can prescribe medications to the patients by executing a smart contract that generates the prescription based on metadata - *such as  patient address, quantity and expiration date.* If the patient allows it, the doctor can also have access to his/her historical record of prescribed drugs. Either way, when the medicine is prescribed, if there is already an active prescription for the same drug, the physician is notified and cannot generate the prescription. This prevents a patient from having multiple doctors prescribing the same drug. 

2. **Patient**: when the doctor prescribes a drug to the patient, he/she can purchase it, by sending a purchase request to the pharmacy. To protect his/her own privacy, the patient can decide who to give access to the historical record of prescribed drugs. 
3. **Pharmacy**: Authenticated pharmacies can disburse the drug after the patient's purchase request has gone through. Once they have checked the prescription ID and the quantity requested by the patient, they can sell the drug and close the transaction. 

## Contracts

This process is allowed by two contracts: 

> **whitelist** 
> **prescriptions**

#### Whitelist
The ***whitelist*** contract is used to manage users - *doctors, patients, pharmacies* - registered on M.ETH via mappings (address, bool). In particular, only the bitPharma manager can add or remove users, and these mappings will be used in the core contract - *prescriptions* - to verify the addresses. In this way, we will ensure that prescriptions are filled by a registered physician, and drugs are only sold by a certified pharmacy.

#### Prescriptions

Let's investigate our main contract and its functionalities. 

**Prescriptions** are embodied in the stuct *prescriptions*. In particular, we have taken into account the possibility of issuing repeatable prescriptions, i.e. prescriptions that allow the same prescription to be dispensed more than once. For this reason we added some variables such as the purchase_cooldown to allow the doctor to set a time before which the patient cannot re-purchase the medicine; e.g. one pack per month for a 6 months period. 

Specifically, the struc **prescription** is characterized by the following attributes: 

 1. *drug*: name of the drug to be prescribed
 2.  *quantity*: total quantity of the drug claimable before the prescription expires
 3. *quantity_claimed*: quantity claimed by user in a single purchase 
 4. *maxclaim*: max amount claimable in single purchase. E.g. the doctor can set a limit to 1 package of the drug each purchase.
 5. *purchase_cooldown*: number of days for the patient to be able to buy the drug again. 
 6. *last_purchase*: timestamp of latest purchase
 7. *expiration*: days from when prescription was issued
 8. *status*: it can take value from 0 to 3 based on the status of the prescription. In particular,  0 means that the prescription has been issued. It takes value 1 once the patient has confirmed the purchase and 2 when the pharmacy has closed the transaction successfully. Finally, if the prescription expires before being used, the status takes value 3.
 9. *doctor*: doctor who issued the prescription
