### Privacy and Security concerns

- **Remove use of a public key in the interface**: at the moment in the interface it is enough to insert the public key of the users to perform transactions on their behalf. This brings extreme risks in terms of security, and should not be **absolutely** used on production. In future developments we will aim to solve this issue, by connecting the interface with Ethereum wallets that are proven to be secure, in order to make BitPharma even more accessible. 
- **Allow some functionalities only to law enforcement**: regarding the functions `get_prescription_pharmacies` and `get_prescription_pharmacy_quantity`, which allow to visualize the history of the medicines sold by each pharmacy, in future developments we will make them visible only to law enforcement agencies for privacy purposes. 

---

### Considerations on efficiency and cost-effectiveness

 - For efficiency reasons, we removed all functions that could have infinite loops, and replaced them with mapping or nested mapping structures. Specifically, we replaced the `check_duplicate_prescriptions` function with `check_active_prescriptions` in commit [8d2b6bfc4f00114616b3591556315a916a950a14](https://github.com/jerryfane/bitpharma/commit/8d2b6bfc4f00114616b3591556315a916a950a14), and rewrote the `patient_prescriptions` function in commit [5fd5bd85f25b3677e65b98741be42944427b7a7a](https://github.com/jerryfane/bitpharma/commit/5fd5bd85f25b3677e65b98741be42944427b7a7a#diff-c87fd0bd7b941c474e85dd0325b831987fdae1d8d27c88bc14d973c937032b4b). Unfortunately in this last case, the function `patient_prescriptions` now shows all the patient's prescriptions, so the history of all his prescriptions for the patient, while previously only the active prescriptions. However, we can check the active prescriptions by using the `prescription_details` function. 

---

### Interface concerns

 - We built the interface with python with the `tkinter` and `web3` packages. It is a rough prototype and it should just express in a simple way how our platform should work. It is run in a local host with ganache. First issue is due to this platform. For the authentication method we relied on the public key: on the backend the default account on web3 is set according to the public key. This could lead to several issues since everybody can have access to the others public keys. 
 - Second issue is due to the web3 package: we have inserted several require with a specific debugging error in the contract. However, instead of giving the error message we insert in the contract, the web3 package gives us a general error. For this reason, in the interface we reflect this and hence, it is harder for the user to understand to the origin of the mistake.

---

### Ideas for further development

- Checks compliance to legislation (e.g. expiration, maximum purchasable quantities...), for specific drugs, perhaps by connecting with an external database
- Implement in some way the possibility for law enforcement to get limited readership rights on patient's prescription history,  when it is needed to investigate cases of illegal prescriptions.
- Insert new features in order to take advantage of the events we have created in the contract. In this way, when a user completes a transaction, e.g. new prescription or purchase, he/she receives a notification.
- It would also make it possible for authorities to track which farmacies are selling which drugs to whom, to help prevent and tackle under the counter sales by matching the outflows with invetory data.

