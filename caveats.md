### Privacy and Security concerns

- **Remove use of a public key in the interface**: at the moment in the interface it is enough to insert the public key of the users to perform transactions on their behalf. This brings extreme risks in terms of security, and should not be **absolutely** used on production. In future developments we will aim to solve this issue, by connecting the interface with Ethereum wallets that are proven to be secure, in order to make BitPharma even more accessible. 
- **Allow some functionalities only to law enforcement**: regarding the functions `get_prescription_pharmacies` and `get_prescription_pharmacy_quantity`, which allow to visualize the history of the medicines sold by each pharmacy, in future developments we will make them visible only to law enforcement agencies for privacy purposes. 

---

### Considerations on efficiency and cost-effectiveness

 - For efficiency reasons, we removed all functions that could have infinite loops, and replaced them with mapping or nested mapping structures. Specifically, we replaced the `check_duplicate_prescriptions` function with `check_active_prescriptions` in commit [8d2b6bfc4f00114616b3591556315a916a950a14](https://github.com/jerryfane/bitpharma/commit/8d2b6bfc4f00114616b3591556315a916a950a14), and rewrote the `patient_prescriptions` function in commit [5fd5bd85f25b3677e65b98741be42944427b7a7a](https://github.com/jerryfane/bitpharma/commit/5fd5bd85f25b3677e65b98741be42944427b7a7a#diff-c87fd0bd7b941c474e85dd0325b831987fdae1d8d27c88bc14d973c937032b4b). Unfortunately in this last case, the function `patient_prescriptions` now shows all the patient's prescriptions, so the history of all his prescriptions for the patient, while previously only the active prescriptions. However, we can check the active prescriptions by using the `prescription_details` function. 

---

### Ideas for further development

- Checks compliance to legislation (e.g. expiration, maximum purchasable quantities...), for specific drugs, perhaps by connecting with an external database
- Implement in some way the possibility for law enforcement to get limited readership rights on patient's prescription history,  when it is needed to investigate cases of illegal prescriptions.

