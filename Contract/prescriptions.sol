pragma solidity >=0.5.0 <0.6.0;

import "./whitelist.sol";

contract bitpharma {

    address bitpharma_manager;
    address whitelist_address; // address of the whitelist contract

    constructor  () public {
        // initialize BitPharma Manager
        // this is the centralized authority used to add new doctors and pharmacies

        bitpharma_manager = msg.sender;
    }

    event Prescribed(string _drug, uint _quantity, uint _maxclaim, uint _purchaseCooldown, uint _daysToExpiration, address _patient);
    event Transaction(uint _prescrId, uint _quantity); // a purchase has been made, as confirmed by both parties
    event Closed(uint _prescrId); // a prescription contract has been closed
    event ReaderAdded(address _reader, address _patient); // a new doctor is added to the list of readers
    event ReaderRemoved(address _reader, address _patient); // a doctor is removed from the list of readers

    struct prescription {
        string drug; // name of the drug prescribed
        uint quantity;  // total quantity of the drug claimable before prescription expires;
        uint quantity_claimed; // quantity claimed by user in the latest purchase
        uint maxclaim; // max quantity claimable in a single purchase
        uint purchase_cooldown; //time (days) needed for the patient to be able to buy the drug again
        uint last_purchase; // timestamp of the latest purchase
        uint expiration; // time left in days
        uint status; // status legend:
        // 0-> prescription is issued
        // 1-> patient confirms purchase
        // 2-> pharma closed transaction successfully
        // 3-> prescription has expired (before all quantity has been claimed)
        address doctor; // doctor who issued the prescription
        }

    prescription[] internal prescriptions;  // array of prescriptions
    mapping (uint => address) internal prescription_to_patient; // for each prescription ID, map to patient address
    mapping (address => uint) internal active_prescriptions; // number of active prescriptions, given patient address
    mapping(address => mapping(address => bool)) internal patient_readers; // addresses who can access patient information
    mapping(address => mapping(bytes32 => bool)) internal patient_active_prescriptions; // drug hash of active prescriptions for each patient
    mapping(address => uint[]) internal patient_id_prescriptions; // id of prescriptions (current and past) for each patient
    mapping(uint => mapping(address => uint[])) prescription_to_pharmacy_quantity; // for each prescription ID, map to the pharmacy who closed it and to the quantity
    mapping(uint => address[]) prescription_to_pharmacy; // for each prescription ID, map to the array of pharmacy who closed it
	
    function lowercase(string memory _str) internal pure returns (string memory) {

        // CREDITS: https://gist.github.com/thomasmaclean/276cb6e824e48b7ca4372b194ec05b97

		bytes memory bytes_str = bytes(_str);
		bytes memory bytes_lower_str = new bytes(bytes_str.length);
		for (uint i = 0; i < bytes_str.length; i++) {
			// if uppercase character...
			if ((uint8(bytes_str[i]) >= 65) && (uint8(bytes_str[i]) <= 90)) {
				// we add 32 to make it lowercase
				bytes_lower_str[i] = bytes1(uint8(bytes_str[i]) + 32);
			} else {
				bytes_lower_str[i] = bytes_str[i];
			}
		}
		return string(bytes_lower_str);
	}
	
    function set_whitelist_address(address _wl_address) external {
        // BitPharma can always update the address of the whitelist contract
        require(msg.sender == bitpharma_manager, "Only BitPharma Manager can update the whitelist address");

        whitelist_address = _wl_address;
    }

    function patient_add_reader(address _reader) external {
        // patients can allow new addresses to access their information (usually doctors)
        require(bitpharma_wl(whitelist_address).patients(msg.sender), "You are not a patient!");

        patient_readers[msg.sender][_reader] = true;
        emit ReaderAdded(_reader, msg.sender);
    }

    function patient_remove_reader(address _reader) external {
        // patients can revoke addresses the access to their information (usually doctors)
        require(bitpharma_wl(whitelist_address).patients(msg.sender), "You are not a patient!");

        patient_readers[msg.sender][_reader] = false;
        emit ReaderRemoved(_reader, msg.sender);
    }

    function new_prescription(string calldata _drug, uint _quantity, uint _maxclaim, uint _purchaseCooldown, uint _daysToExpiration, address _patient) external {
        // a whitelisted doctor can issue a new prescriptions to a valid patient address
        require(bitpharma_wl(whitelist_address).doctors(msg.sender), "Only doctors can issue new prescriptions!");
        require(bitpharma_wl(whitelist_address).patients(_patient), "This address does not match any patient");
        require(_daysToExpiration < 90, "You can't issue prescriptions for such long period of time");
        // further checks:
        require( _purchaseCooldown*(_quantity/_maxclaim) <= _daysToExpiration, "Something is wrong please check...");
        require(check_active_prescriptions(_patient,_drug) == false, "The patient already has an active prescription for this drug");

        uint id = prescriptions.push(prescription(lowercase(_drug), _quantity, 0, _maxclaim, _purchaseCooldown * 1 days, 0, now + _daysToExpiration * 1 days , 0, msg.sender)) - 1;
        prescription_to_patient[id] = _patient;
        active_prescriptions[_patient]++;
        patient_readers[_patient][_patient] = true;
        patient_active_prescriptions[_patient][keccak256(bytes(lowercase(_drug)))] = true;
        patient_id_prescriptions[_patient].push(id);
        emit Prescribed(_drug,_quantity,_maxclaim,_purchaseCooldown,_daysToExpiration,_patient);
    }

    function patient_purchasing(uint _prescrId, uint _quantity) external {
        // patient confirms the purchase of his/her own prescribed drug
        require(msg.sender == prescription_to_patient[_prescrId], "You don't have the right to access this prescription!");
        require(prescriptions[_prescrId].status==0, "You can't confirm purchase for this item!");
        // further checks:
        require(prescriptions[_prescrId].maxclaim>=_quantity, "You can't buy this much in a single purchase");
        require(prescriptions[_prescrId].quantity>=_quantity, "Claim exceeds quantity left...");
        require(prescriptions[_prescrId].last_purchase + prescriptions[_prescrId].purchase_cooldown<= now, "Wait a few more before buying again");

        address patient = prescription_to_patient[_prescrId];
        string memory drug = prescriptions[_prescrId].drug;

        if(now>prescriptions[_prescrId].expiration) { // if that prescription has expired, change its status (????)
            prescriptions[_prescrId].status=3;
            active_prescriptions[prescription_to_patient[_prescrId]]--;
            patient_active_prescriptions[patient][keccak256(bytes(lowercase(drug)))] = false;
        }
        else {
            prescriptions[_prescrId].status=1;
            prescriptions[_prescrId].quantity_claimed=_quantity;
        }
    }

    function close_transaction(uint _prescrId, uint _quantity) external {
        // whitelisted pharmacy can close transaction after patient has confirmed purchase
        require(bitpharma_wl(whitelist_address).pharmacies(msg.sender), "Only pharmacies can close transactions!");
        require(prescriptions[_prescrId].status==1, "This transaction can't be confirmed!");
        require(prescriptions[_prescrId].quantity_claimed==_quantity, "Agree with the patient on the quantity claimed");

        address patient = prescription_to_patient[_prescrId];
        string memory drug = prescriptions[_prescrId].drug;

        if (prescriptions[_prescrId].quantity - _quantity > 0 ){ // if some quantity left after this purchase
            prescriptions[_prescrId].status = 0;
            prescriptions[_prescrId].quantity = prescriptions[_prescrId].quantity - _quantity;
        }
        else { // if no quantity left after this purchase
            prescriptions[_prescrId].status = 2;
            active_prescriptions[patient]--;
            patient_active_prescriptions[patient][keccak256(bytes(lowercase(drug)))] = false;
            emit Closed(_prescrId);
        }
        prescriptions[_prescrId].last_purchase=now;
        prescription_to_pharmacy_quantity[_prescrId][msg.sender].push(_quantity);
        prescription_to_pharmacy[_prescrId].push(msg.sender);
        emit Transaction(_prescrId, _quantity);
    }

    function patient_prescriptions(address _patient) external view returns(uint[] memory) {
        // returns the ids of a specific patient's prescriptions
        // can only be accessed by readers, which the patient him/herself can nominate (and revoke)
        require(patient_readers[_patient][msg.sender], "You can't access prescriptions!");
        return patient_id_prescriptions[_patient];
    }

    function check_active_prescriptions(address _patient, string memory _drug) internal view returns(bool) {
        // returns whether a prescription is currently active for a specific patient and a specific drug
        // only used within NewPrescription, to make sure multiple prescriptions do not occur, and not as a mean to gather sensitive personal information.

        return patient_active_prescriptions[_patient][keccak256(bytes(lowercase(_drug)))];
    }

    function prescription_details(uint _prescrId) external view returns(string memory drug, uint quantity_left, uint max_claim, bool can_I_buy, uint days_to_expiration, uint status) {
        // prints out detail for a specific prescription
        // can only be accessed by:
        require(patient_readers[prescription_to_patient[_prescrId]][msg.sender] // readers for that prescription's recipient
                || msg.sender==prescriptions[_prescrId].doctor  // the doctor who issued the prescription
                || bitpharma_wl(whitelist_address).pharmacies(msg.sender), // pharmacies (all???)
                "You can't see this prescription!");
        drug = prescriptions[_prescrId].drug;
        quantity_left = prescriptions[_prescrId].quantity;
        max_claim = prescriptions[_prescrId].maxclaim;
        can_I_buy = (prescriptions[_prescrId].purchase_cooldown+prescriptions[_prescrId].last_purchase < now);
        days_to_expiration = ((prescriptions[_prescrId].expiration - now) / 86400);
        status = prescriptions[_prescrId].status;
    }

    function get_prescription_pharmacies(uint _prescId) external view returns(address[] memory) {
        return prescription_to_pharmacy[_prescId];
    }

    function get_prescription_pharmacy_quantity(uint _prescId, address _pharmacy) external view returns(uint[] memory) {
        return prescription_to_pharmacy_quantity[_prescId][_pharmacy];
    }


}