pragma solidity >=0.5.0 <0.6.0;

contract bitpharma {

    address doctor;
    address patient;
    address pharmacy;

    constructor  (address _doctor, address _patient, address _pharmacy) public {
        //to initialize addresses
        doctor = _doctor;
        patient = _patient;
        pharmacy = _pharmacy;
    }

    struct prescription {
        string drug;
        uint quantity;  //total quantity of the drug claimable before prescription expires;
        uint quantity_claimed; //quantity claimed by user in a single purchase
        uint maxclaim; //max amount claimable in single purchase
        uint purchase_cooldown; //set in days for the patient to be able to buy the drug again
        uint last_purchase; //timestamp of latest purchase
        uint expiration; //days from when prescription was issued
        uint status; //status legend: 0-> prescription is issued, 1-> patient confirms purchase,
        //2-> pharma clossed transaction successfully, 3-> prescription expired before purchase...

        //bool exists;
        }

    prescription[] internal prescriptions;  //array of prescriptions
    mapping (uint => address) internal prescription_to_patient; //for each prescription ID, map to patient address
    mapping (address => uint) internal active_prescriptions; //number of active prescriptions given patient address

    function newPrescription(string calldata _drug, uint _quantity, uint _maxclaim, uint _purchaseCooldown, uint _daysToExpiration, address _patient) external {  //only doctors can add elements in the array
        require(msg.sender == doctor, "Only doctors can issue new prescriptions!");
        require(_patient == patient, "Please indicate a valid patient!");
        require(_daysToExpiration < 90, "You can't issue prescriptions for such long period of time");
        require( _purchaseCooldown*(_quantity/_maxclaim) <= _daysToExpiration, "Something is wrong please check...");
        uint id = prescriptions.push(prescription(_drug, _quantity, 0, _maxclaim, _purchaseCooldown * 1 days, 0, now + _daysToExpiration * 1 days ,0)) - 1;
        prescription_to_patient[id] = _patient;
        active_prescriptions[_patient]++;
    }

    function patient_purchasing(uint _prescrId, uint _quantity) external {  //patient can confirm the purchase of a prescription in the array
        require(msg.sender == prescription_to_patient[_prescrId], "You don't have the right to access this prescription!");
        require(prescriptions[_prescrId].status==0, "You can't confirm purchase for this item!");
        require(prescriptions[_prescrId].maxclaim>=_quantity, "You can't buy this much in a single purchase");
        require(prescriptions[_prescrId].quantity>=_quantity, "Claim exceeds quantity left...");
        require(prescriptions[_prescrId].last_purchase + prescriptions[_prescrId].purchase_cooldown<= now, "Wait a few more before buying again");
        if(now>prescriptions[_prescrId].expiration) {
            prescriptions[_prescrId].status=3;
            active_prescriptions[prescription_to_patient[_prescrId]]--;
        }
        else {
            prescriptions[_prescrId].status=1;
            prescriptions[_prescrId].quantity_claimed=_quantity;
        }
    }

    function close_transaction(uint _prescrId, uint _quantity) external {  //pharmacies can close transactions after patient has confirmed purchase
        require(msg.sender == pharmacy, "Only pharmacies can close transactions!");
        require(prescriptions[_prescrId].status==1, "This transaction can't be confirmed!");
        require(prescriptions[_prescrId].quantity>=_quantity, "The doctor did not release enough quantity");  //possiamo cancellarlo perchè incluso nel successivo (?)
        require(prescriptions[_prescrId].quantity_claimed==_quantity, "Agree with the patient on the quantity claimed");

        if (prescriptions[_prescrId].quantity - _quantity > 0 ){
            prescriptions[_prescrId].status = 0;
            prescriptions[_prescrId].quantity = prescriptions[_prescrId].quantity - _quantity;
        }
        else {
            prescriptions[_prescrId].status = 2;
            active_prescriptions[prescription_to_patient[_prescrId]]--;
        }
        prescriptions[_prescrId].quantity_claimed=0;
        prescriptions[_prescrId].last_purchase=now;
    }


    function my_prescriptions() external view returns(uint[] memory list_of_myPrescriptions_Ids) {  //return all active prescriptions IDs of a patient
        require(msg.sender==patient, "You can't access prescriptions!");
        uint[] memory result = new uint[](active_prescriptions[msg.sender]);
        uint counter = 0;
        for (uint i = 0; i < prescriptions.length; i++) {
            if (prescription_to_patient[i] == msg.sender && prescriptions[i].status<2) {
                result[counter] = i;
                counter++;
            }
        }
        list_of_myPrescriptions_Ids = result;
        //return result;
    }
    
    
    function prescription_details(uint _prescrId) external view returns(string memory drug, uint quantity_left, uint max_claim, bool can_I_buy, uint time_to_expiration, uint status) {
        require(msg.sender==prescription_to_patient[_prescrId], "You can't see this prescription!");
        drug = prescriptions[_prescrId].drug;
        quantity_left = prescriptions[_prescrId].quantity;
        max_claim = prescriptions[_prescrId].maxclaim;
        can_I_buy = (prescriptions[_prescrId].purchase_cooldown+prescriptions[_prescrId].last_purchase < now);
        time_to_expiration = prescriptions[_prescrId].expiration - now;
        status = prescriptions[_prescrId].status;

        //return (prescriptions[_prescrId].drug, prescriptions[_prescrId].quantity, prescriptions[_prescrId].maxclaim, (prescriptions[_prescrId].purchase_cooldown+prescriptions[_prescrId].last_purchase < now), prescriptions[_prescrId].expiration - now, prescriptions[_prescrId].status);
    }


    //just to print stuff
    function getdoctor() external view returns(address) {
        return doctor;
    }

    function getpatient() external view returns(address) {
        return patient;
    }

    function getpharma() external view returns(address) {
        return pharmacy;
    }

    //function gettimestamp() external view returns(uint) {
    //    return now;
    //}

}