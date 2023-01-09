// SPDX-License-Identifier: GPL-3.0
pragma solidity ^0.8.0;
import '@openzeppelin/contracts/token/ERC721/ERC721.sol';
import '../Libraries/Ownable.sol';
import './DTtoken.sol';


/*
//The smart contract showes an example of subscription for the DecentralTrading market application. It implements the ERC721 interface
provided by the OpenZeppelin library. The interface is tipically used for NFT implementations. The other interface implemented 
is Ownable, which set the user who deploy the contract as owner.
*/
contract DTsubscription is ERC721, Ownable {
  //Name of the NFT subscription 
  string public constant name_ = "DTsubscription";
  //Symbol of the NFT subscription
  string public constant symbol_ = "DTS";
  //Price in DTtoken of the NFT subscription
  uint256 private constant price = 1;
  //Instance of the smart contract handling DTtokens
  DTtoken private dToken;
  //Duration of the subscription
  uint constant subscriptionDuration=30 days;
  //Number of subscriptions generated, used as identifier
  uint private mintedTokens=0;
  //Mapping which relates each id subscription to its identifier
  mapping(uint=>address) tokenOwner;
  //Mapping which relates wach id subcription to the contained information
  mapping(uint=>SubscriptionInfo) idToSubscriptionInfo;
  //Constructor of the smart contract
  constructor(address dtoken) ERC721("DTsubscription","DTS"){
    dToken=DTtoken(dtoken);
  }
  //Method exchange an amount of DTtoknes of the caller user, with a new DTsubscription
  function purchaseSubscription() public  returns(uint)
  {
    dToken.transferFrom(msg.sender,address(this),price);
    mintedTokens+=1;
    _mint(msg.sender,mintedTokens);
    tokenOwner[mintedTokens]=msg.sender;
    idToSubscriptionInfo[mintedTokens]=SubscriptionInfo(block.timestamp,block.timestamp + subscriptionDuration,SubscriptionType.FULL_SUBSCRIPTION);
    return mintedTokens;
  }

  function _transfer(address _from, address _to, uint256 _tokenId) override internal 
  {

  }
  // The method verifies that the input DTsubscription ID is still valid.
  function isSubscriptionActive(uint256 _tokenId) public view returns (bool state){
    SubscriptionInfo memory token = idToSubscriptionInfo[_tokenId];
    if(token.expiresOn<block.timestamp){return false;}
    else{return true;}
  }
  /*
  The method check if the input DTsubscription ID is related to an active subscription,
   owned by the inuput claim_owner
   */
  function verify_subscription(uint256 _tokenId,address claim_owner)public view returns(bool){
    address real_owner=tokenOwner[_tokenId];
    return isSubscriptionActive(_tokenId) && real_owner==claim_owner;

  }
  /*
  The method retrieve all the DTsubscriptions related to the input address
   */
  function get_subscriptions(address addr) public view returns(uint[] memory)
  {

    uint256 final_counter=0;
    for(uint i=1;i<=mintedTokens;i++){
      if(tokenOwner[i]==addr){final_counter++;}
    }
    uint[] memory final_result=new uint[](final_counter);
    uint256 j=0;
      for(uint i=1;i<=mintedTokens;i++){
         if(tokenOwner[i]==addr){final_result[j]=i;j++;}
    }
    return final_result;
  }
  /*
  Enum which express the subscription type. Actually we have only one type of subscriptions
   */
enum SubscriptionType{FULL_SUBSCRIPTION}
  /*
  Struct containing the DTsubscription's information.
   */
struct SubscriptionInfo {

    uint registeredOn;
    uint expiresOn;
    SubscriptionType subscriptionType;

}


}
