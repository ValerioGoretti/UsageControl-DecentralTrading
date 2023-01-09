// SPDX-License-Identifier: GPL-3.0

pragma solidity ^0.8.0;
import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "../Libraries/Ownable.sol";
/*
The DTtoken smart contract implement a ERC20 token (fungible token). 
The token is the only currency considered by the DecentralTrading market.
*/
contract DTtoken is ERC20,Ownable {
     /*
     Constructor of the class.
    */
    constructor() ERC20("DTtoken","DT") {}
    /*
    Function used by the owner of the smart contract. 
    It is used to generate new DTtokens in the balance of the input account.
    */
    function mint(address account, uint256 amount) public onlyOwner returns (bool) 
    {
        _mint(account, amount);
        return true;
    }
    /*
    It is used to generate new DTtokens in the balance of the input account.
    */
    function burn(address account,uint256 amount) public onlyOwner virtual 
    {
        _burn(account, amount);
    }


    

}