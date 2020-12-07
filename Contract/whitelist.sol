pragma solidity >=0.5.0 <0.6.0;

contract bitpharma_wl {

    address bitpharma_manager;

    constructor  () public {
        //initialize BitPharma Manager
        //this is the centralized authority used to add new doctors and pharmacies
        bitpharma_manager = msg.sender;
    }

    mapping (address => bool) public doctors; //tuple for doctors affiliated with BitPharma
    mapping (address => bool) public pharmacies; //tuple for pharmacies affiliated with BitPharma

    function add_doctor(address _doctor) public {
        require(msg.sender == bitpharma_manager, "Only BitPharma can add new doctors");
        doctors[_doctor] = true;
    }

    function add_pharmacy(address _pharmacy) public {
        require(msg.sender == bitpharma_manager, "Only BitPharma can add new pharmacies");
        pharmacies[_pharmacy] = true;
    }

    function is_doctor(address _doctor) external view returns (bool){
        return doctors[_doctor];
    }

    function is_pharmacy(address _pharmacy) external view returns (bool){
        return pharmacies[_pharmacy];
    }

}
