# M.ETH - Medical (Prescriptions) on Ethereum

In Italy, a lot of medical prescriptions are still hand written: electronic prescription are only required when the drug is paid by the regional public system, but every pharmaceutical drug that legally requires a medical prescription can still be bought with a hand-written prescription. This leads to an **authenticity problem**. Moreover, it is common practice that a pharmacist does not ask for medical prescription, even if it is needed. These behaviors cause a serious problem of **drug use disorders** among the population. This project has the aim of overcoming these kind of issues. 

This service consists in a **blockchain application** that authenticates medical prescriptions and facilitates the interoperability between medical doctors, pharmacies and authorities, creating an aggregate prescription-drugs-database in a secure way.

Prescriptions that are transmitted using the blockchain platform can be verified together with the identities of the medical doctor and the patient. Pharmacists would then be able to verify the authenticity of the prescription to ensure that they are selling a medicine for legitimate use. 

Blockchain would also overcome the issue of **privacy** for health data, as patient's information would be de-identified, so that only trusted viewers, selected by the patient, can associate the patient with the records present in the blockchain.

## Overview - how it works

Doctors, patients and pharmacies can **register** on M.Eth by entering their information, e.g. their Social Security number.  Once registered, doctors can **prescribe** medicines to patients with various indications, such as the max amount of packages claimable in a single purchase. 
When the patient wants to purchase the medicine, he/she can send a **purchase request**, and once it has been submitted, the pharmacy can **close** the prescription and sell the medicine to the patient. 

Throughout the entire process, patients' **privacy** is protected. Indeed, they will be the only ones who can decide who has access to their information and their list of prescriptions.

The **roles** defined in the project are the following:

 1. **Doctor**: the doctor can prescribe medications to the patients by executing a smart contract that generates the prescription based on metadata - *such as  patient address, quantity and expiration date.* If the patient allows it, the doctor can also have access to his/her historical record of prescribed drugs. Either way, when the medicine is prescribed, if there is already an active prescription for the same drug, the physician is notified and cannot generate the prescription. This prevents a patient from having multiple doctors prescribing the same drug. 

2. **Patient**: when the doctor prescribes a drug to the patient, he/she can purchase it, by sending a purchase request to the pharmacy. To protect his/her own privacy, the patient can decide who to give access to the historical record of prescribed drugs. 
3. **Pharmacy**: Authenticated pharmacies can disburse the drug after the patient's purchase request has gone through. Once they have checked the prescription ID and the quantity requested by the patient, they can sell the drug and close the transaction. 
