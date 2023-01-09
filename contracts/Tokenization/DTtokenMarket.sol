
//SPDX-License-Identifier: GPL-3.0
pragma solidity ^0.8.0;

import "./DTtoken.sol";
/*
Smart contract used to distribute DTtokens, by exchanging them with ETH(Wei).
*/
contract DTtokenMarket 
{
    /*
    Reference to the DTtoken smart contract of the infrastructure
    */
    DTtoken dToken;
    /*
    Value of a DTtoken in Wei
    */
    uint public weiValue;
    /*
    Constructor of the class.
    */
    constructor(address tokenAddress){
      dToken=DTtoken(tokenAddress);
      weiValue=500000000000000;
    }
    /*
    Modifier that check if the input amount of DTtokens is available in the smart contract balance.
    */
    modifier areTokensAvailable(uint requiredTokens) 
    {
      require(dToken.balanceOf(address(this))>=requiredTokens,
      "The requested amount is not available");
      _;
    }
    /*
    Modifier that check if the needed Ether of the message is sufficient to perform the exchange.
    */  
    modifier isEtherEnough(uint etherAmount, uint neededEther) 
    {
      require(etherAmount>=neededEther,
      "Insufficient amount of ether");
      _;
    }
    /*
    Function that exchange Ether with DTtokens.
    */ 
    function buyTokens(uint amount) areTokensAvailable(amount) isEtherEnough(msg.value,weiValue*amount)  payable public returns (bool success){
        dToken.transfer(msg.sender,amount);
        return true;
    }
}