pragma solidity >=0.5.0 <0.6.0;

import "./whitelist.sol";
import {utils}  from "./bitpharma_utils.sol";


contract bitpharma {

    using utils for string;

    // restrict the deployment to only doctors?
    address bitpharma_manager;
    address whitelist_address; //whitelist  address is the address of the whitelist contract

    constructor  () public {
        //initialize BitPharma Manager
        //this is the centralized authority used to add new doctors and pharmacies
        bitpharma_manager = msg.sender;
    }

    // these events will be generated when transaction is mined (and hopefully we will catch them with Python)
    event Prescribed(string _drug, uint _quantity, uint _maxclaim, uint _purchaseCooldown, uint _daysToExpiration, address _patient);
    event Transaction(uint _prescrId, uint _quantity); // a purchase has been made, as confirmed by both parties
    event Closed(uint _prescrId); // a prescription contract has been closed
    event ReaderAdded(address _reader, address _patient); // a new doctor is added to the list of readers
    event ReaderRemoved(address _reader, address _patient); // a doctor is removed from the list of readers

    struct prescription {
        string drug;
        uint quantity;  //total quantity of the drug claimable before prescription expires;
        uint quantity_claimed; //quantity claimed by user in a single purchase ??
        uint maxclaim; //max amount claimable in single purchase
        uint purchase_cooldown; //set in days for the patient to be able to buy the drug again
        uint last_purchase; //timestamp of latest purchase
        uint expiration; //days from when prescription was issued
        uint status; //status legend: 0-> prescription is issued, 1-> patient confirms purchase,
        //2-> pharma closed transaction successfully, 3-> prescription expired before purchase...
        address doctor; //Doctor who issued the prescription
        }

    prescription[] internal prescriptions;  //array of prescriptions
    mapping (uint => address) internal prescription_to_patient; //for each prescription ID, map to patient address
    mapping (address => uint) internal active_prescriptions; //number of active prescriptions given patient address
    mapping(address => mapping(address => bool)) internal patient_readers; //addresses who can access patient information
    mapping(address => mapping(bytes32 => bool)) internal patient_active_prescriptions; //drug hash of active prescriptions for each patient


    function set_whitelist_address(address _wl_address) external {
        //BitPharma can always update the address of the whitelist contract
        require(msg.sender == bitpharma_manager, "Only BitPharma Manager can update the whitelist address");
        whitelist_address = _wl_address;
    }

    function patient_add_reader(address _reader) external {
        //patients can allow new addresses to access their information (usually doctors)
        require(bitpharma_wl(whitelist_address).patients(msg.sender), "You are not a patient!");
        patient_readers[msg.sender][_reader] = true;
        emit ReaderAdded(_reader, msg.sender);
    }

    function patient_remove_reader(address _reader) external {
        //patients can remove addresses the access to their information (usually doctors)
        require(bitpharma_wl(whitelist_address).patients(msg.sender), "You are not a patient!");
        patient_readers[msg.sender][_reader] = false;
        emit ReaderRemoved(_reader, msg.sender);
    }

    function newPrescription(string calldata _drug, uint _quantity, uint _maxclaim, uint _purchaseCooldown, uint _daysToExpiration, address _patient) external {  //only doctors can add elements in the array
        require(bitpharma_wl(whitelist_address).doctors(msg.sender), "Only doctors can issue new prescriptions!");
        require(bitpharma_wl(whitelist_address).patients(_patient), "This address does not match any patient");
        require(_daysToExpiration < 90, "You can't issue prescriptions for such long period of time");
        require( _purchaseCooldown*(_quantity/_maxclaim) <= _daysToExpiration, "Something is wrong please check...");
        require(check_active_prescriptions(_patient,_drug) == false, "The patient already has an active prescription for this drug");
        uint id = prescriptions.push(prescription(utils.lowercase(_drug), _quantity, 0, _maxclaim, _purchaseCooldown * 1 days, 0, now + _daysToExpiration * 1 days , 0, msg.sender)) - 1;
        prescription_to_patient[id] = _patient;
        active_prescriptions[_patient]++;
        patient_readers[_patient][_patient] = true;
        patient_active_prescriptions[_patient][keccak256(bytes(utils.lowercase(_drug)))] = true;
        emit Prescribed(_drug,_quantity,_maxclaim,_purchaseCooldown,_daysToExpiration,_patient);
    }

    function patient_purchasing(uint _prescrId, uint _quantity) external {
        //patient can confirm the purchase of a prescription in the array
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

    function close_transaction(uint _prescrId, uint _quantity) external {
        //pharmacies can close transactions after patient has confirmed purchase
        require(bitpharma_wl(whitelist_address).pharmacies(msg.sender), "Only pharmacies can close transactions!");
        require(prescriptions[_prescrId].status==1, "This transaction can't be confirmed!");
        require(prescriptions[_prescrId].quantity_claimed==_quantity, "Agree with the patient on the quantity claimed");
        address patient = prescription_to_patient[_prescrId];
        string memory drug = prescriptions[_prescrId].drug;

        if (prescriptions[_prescrId].quantity - _quantity > 0 ){
            prescriptions[_prescrId].status = 0;
            prescriptions[_prescrId].quantity = prescriptions[_prescrId].quantity - _quantity;
        }
        else {
            prescriptions[_prescrId].status = 2;
            active_prescriptions[patient]--;
            patient_active_prescriptions[patient][keccak256(bytes(utils.lowercase(drug)))] = false;
            emit Closed(_prescrId);
        }
        //prescriptions[_prescrId].quantity_claimed=0; maybe useless
        prescriptions[_prescrId].last_purchase=now;
        emit Transaction(_prescrId, _quantity);
    }


    function patient_prescriptions(address _patient) external view  returns(uint[] memory list_of_Prescriptions_Ids) {
        require(patient_readers[_patient][msg.sender], "You can't access prescriptions!");
        uint[] memory result = new uint[](active_prescriptions[_patient]);
        uint counter = 0;
        for (uint i = 0; i < prescriptions.length; i++) {
            if (prescription_to_patient[i] == _patient && prescriptions[i].status<2) {
                result[counter] = i;
                counter++;
            }
        }
        list_of_Prescriptions_Ids = result;
    }

    function check_active_prescriptions(address _patient, string memory _drug) internal view returns(bool) {
        return patient_active_prescriptions[_patient][keccak256(bytes(utils.lowercase(_drug)))];
    }

    function prescription_details(uint _prescrId) external view returns(string memory drug, uint quantity_left, uint max_claim, bool can_I_buy, uint days_to_expiration, uint status) {
        require(patient_readers[prescription_to_patient[_prescrId]][msg.sender] || msg.sender==prescriptions[_prescrId].doctor || bitpharma_wl(whitelist_address).pharmacies(msg.sender), "You can't see this prescription!");
        drug = prescriptions[_prescrId].drug;
        quantity_left = prescriptions[_prescrId].quantity;
        max_claim = prescriptions[_prescrId].maxclaim;
        can_I_buy = (prescriptions[_prescrId].purchase_cooldown+prescriptions[_prescrId].last_purchase < now);
        days_to_expiration = ((prescriptions[_prescrId].expiration - now) / 86400);
        status = prescriptions[_prescrId].status;
    }


}
