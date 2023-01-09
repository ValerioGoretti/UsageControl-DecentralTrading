// SPDX-License-Identifier: GPL-3.0
pragma solidity >=0.7.0 <0.9.0;
abstract contract Ownable 
{    
    address private _owner;

 
 
    /**
     Initializes the contract setting the deployer as the initial owner.
     */
    constructor() {
        _owner=msg.sender;
    }

    /**
     Throws if called by any account other than the owner.
     */
    modifier onlyOwner() {
         require(_owner== msg.sender, "Ownable: caller is not the owner");
        _;
    }

    function owner() public view virtual returns (address) {
        return _owner;
    }

    /**
    Transfers ownership of the contract to a new account (`newOwner`).
     * Can only be called by the current owner.
     */
    function transferOwnership(address newOwner) public virtual onlyOwner {
        require(newOwner != address(0));
         _owner = newOwner;
    }

  
}