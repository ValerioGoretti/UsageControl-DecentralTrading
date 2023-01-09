// SPDX-License-Identifier: GPL-3.0
pragma solidity ^0.8.0;
import "../Tokens/DTsubscription.sol";
import "../Policies/DTobligations.sol";
  /*
  The smart contract is part of the Indexing module. The smart contract contains the logic to manage pods and resources'
  metadata. Dara owners and pod managers interact with the DTindexing in order to initialize/deactivate resources.
  Metadata collected in DTindexing are used to coordinate processes in DecentralTrading market.
  Data Consumers interact with the smart contract to retrieve information regarding pods and resources.
  */

  
contract DTindexing
{
    /*
    Counter used to identify pods.
    */
    int private podsCounter=0;
    /*
    Counter used to identify resources
    */
    int private resourceCounter=0;
    /*
    Reference to the DTsubscription smart contract.
    */
    DTsubscription private dtSubscription;
    /*
    List of initialized pods.
    */
    Pod[] private podList;
    /*
    List of initialized resources.
    */
    Resource[] private resourceList;
  /*
  Modifier that checks if the given identifier is valid, related to an active pod. Finally it's checked if the sender
  of the msg is signed with the pod's credentials.
  */
  modifier validPodId(uint id,address owner) 
  {
    require (id<podList.length,"The given id is unknown");
    Pod memory pod= podList[id];
    require(pod.isActive==true,"The pod is not active");
    require (pod.podAddress==owner,"The sender is not the pod");
    _;
  }
  /*
  Modifier that checks if the given resource id is valid and if it is related to an active resource.
  */
  modifier validResourceId(uint id){
    require (id<resourceList.length,"The given id is unknown");
    Resource memory resource= resourceList[id];
    require(resource.isActive==true,"The resource is not active");
    _;
  }
  /*
  Enum that represents the content of a pod.
  */
    enum PodType{FINANCIAL,SOCIAL,MEDICAL}
  /*
  Search functions for Medical pods.
  */
    function getMedicalPods(uint idSubscription) public view returns(Pod[] memory) 
    {
        return searchByType(PodType.MEDICAL);
    }
  /*
  Search functions for Social pods.
  */
     function getSocialPods(uint idSubscription) public view returns(Pod[] memory) 
    {
        return searchByType(PodType.SOCIAL);
    }
  /*
  Search functions for Financial pods.
  */
     function getFinancialPods(uint idSubscription) public view returns(Pod[] memory) 
    {
        return searchByType(PodType.FINANCIAL);
    }
  /*
  Function used to initialize new pods in DecentralTrading. It rquire the WEB reference of the pod service and the 
  pod's credentials.
  */
    function registerPod(bytes memory newReference,PodType podType,address podAddress) public returns(int) 
    { 
       int idPod=podsCounter;
       podList.push(Pod(podsCounter,podType,msg.sender,podAddress,newReference,true));
       DTobligations obligation = new DTobligations(address(this),podAddress);
       emit NewPod(podsCounter,address(obligation));
       podsCounter+=1;
       return idPod;
    }
  /*
  Private method used by the search functions.
  */
  function searchByType(PodType tp) private view returns(Pod[] memory) 
  {
    uint resultCount=0;
    for (uint i = 0; i < podList.length; i++) {
        if (podList[i].podType == tp) {
            resultCount++;  
        }
    }
    uint j;
    Pod[] memory result=new Pod[](resultCount);
    for(uint i=0;i<podList.length;i++){
      if (podList[i].podType==tp){
        result[j]=podList[i];
        j++;
      }

    }
    return result;
  }
  /*
  Get the information of the resources stored into the given pod identifier.
  */
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

  /*
  Function used to initialize new resources in the given pod id. The newReference parameter is the WEB reference of the resource.
  */
  function registerResource(int podId,bytes memory newReference, uint idSubscription) public validPodId(uint(podId),msg.sender) returns(int) 
  {
       int idResource=resourceCounter;
       resourceList.push(Resource(resourceCounter,msg.sender,newReference,podId,true));
       emit NewResource(resourceCounter);
       resourceCounter+=1;
       return idResource;
  }
   /*
  Function that takes as input a resource id and returns the related metadata.
  */ 
  function getResource(int idResource) view public validResourceId(uint(idResource)) returns(Resource memory)
  {
    return resourceList[uint(idResource)];
  }
    /*
  Function used to remove resources from DecentralTrading.
  */
  function deactivateResource(int idResource) public validResourceId(uint(idResource))
  {
    resourceList[uint(idResource)].isActive=false;
  }

 
/*
Event emitted on the generation of a new resource.
*/
event NewResource(int idResource);
/*
Event emitted on the generation of a new pod.
*/
event NewPod(int idPod, address obligationAddress);
/*
Struct representing pods' metadata.
*/
struct Pod
{
  /*
  Identifier of the pod.
  */
  int id;
  /*
  Type of the pod.
  */
  PodType podType;
  /*
  Address of the pod's owner.
  */
  address owner;
  /*
  Credentials associated with the Pod.
  */
  address podAddress;
  /*
  Web reference pointg at the pod's root.
  */
  bytes baseUrl;
  /*
  Boolean flag that marks a pod as active.
  */
  bool isActive;
}
/*
Struct representing resources' metadata.
*/
struct Resource
{ 
  /*
  Identifier of the resource.
  */
  int id;
  /*
  Address of the resource's owner.
  */
  address owner;
  /*
  WEB reference pointing at the resource.
  */ 
  bytes url;
  /*
  Identifier of the pod in wich the resource is stored.
  */   
  int podId;
  /*
  Boolean flag that marks a resource as active.
  */  
  bool isActive;

}
 

  
}