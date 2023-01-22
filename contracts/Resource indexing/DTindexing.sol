// SPDX-License-Identifier: GPL-3.0
pragma solidity ^0.8.0;
import "../Tokenization/DTsubscription.sol";
import "../Policy Governance/DTobligations.sol";
  contract DTindexing
{

    int private podsCounter=0;
    int private resourceCounter=0;
    DTsubscription private dtSubscription;

    Pod[] private podList;
    Resource[] private resourceList;
    address monitoringOracle;
    constructor(address oracleAddress)
    {
      monitoringOracle=oracleAddress;
      podsCounter=0;
      resourceCounter=0;
    }
  modifier validPodId(uint id,address owner) 
  {
    require (id<podList.length,"The given id is unknown");
    Pod memory pod= podList[id];
    require(pod.isActive==true,"The pod is not active");
    require (pod.podAddress==owner,"The sender is not the pod");
    _;
  }

  modifier validResourceId(uint id){
    require (id<resourceList.length,"The given id is unknown");
    Resource memory resource= resourceList[id];
    require(resource.isActive==true,"The resource is not active");
    _;
  }
    enum PodType{FINANCIAL,SOCIAL,MEDICAL}
  
  function registerPod(bytes memory newReference,PodType podType,address podAddress) public returns(int) 
  { 
      int idPod=podsCounter;
      podList.push(Pod(podsCounter,podType,msg.sender,podAddress,newReference,true));
      DTobligations obligation = new DTobligations(address(this),podAddress,monitoringOracle);
      emit NewPod(podsCounter,address(obligation));
      podsCounter+=1;
      return idPod;
  }
  function getPodResources(int pod_id,uint idSubscription) public view returns(Resource[] memory) 
  {
    uint resultCount=0;
    for (uint i = 0; i < resourceList.length; i++) {
        if (resourceList[i].podId==pod_id && resourceList[i].isActive) {
            resultCount++;  
        }
    }
    uint j;
    Resource[] memory result=new Resource[](resultCount);
    for(uint i=0;i<resourceList.length;i++){
    if (resourceList[i].podId==pod_id && resourceList[i].isActive){
      result[j]=resourceList[i];
      j++;
    }

    }
    return result;
  }
  function registerResource(int podId,bytes memory newReference, uint idSubscription) public validPodId(uint(podId),msg.sender) returns(int) 
  {
       int idResource=resourceCounter;
       resourceList.push(Resource(resourceCounter,msg.sender,newReference,podId,true));
       emit NewResource(resourceCounter);
       resourceCounter+=1;
       return idResource;
  }
  function getResource(int idResource) view public validResourceId(uint(idResource)) returns(Resource memory)
  {
    return resourceList[uint(idResource)];
  }
  function deactivateResource(int idResource) public validResourceId(uint(idResource))
  {
    resourceList[uint(idResource)].isActive=false;
  }
event NewResource(int idResource);
event NewPod(int idPod, address obligationAddress);
struct Pod
{
  int id;
  PodType podType;
  address owner;
  address podAddress;
  bytes baseUrl;
  bool isActive;
}
struct Resource
{ 
  int id;
  address owner;
  bytes url;
  int podId;
  bool isActive;

}
 

  
}