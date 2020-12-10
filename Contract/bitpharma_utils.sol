
pragma solidity >=0.5.0 <0.6.0;

contract bitpharma_utils {
	
    function lowercase(string calldata _str) external pure returns (string memory) {

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
}