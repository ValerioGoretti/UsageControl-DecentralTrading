// SPDX-License-Identifier: GPL-3.0
pragma solidity ^0.8.0;
import "../Indexing/DTindexing.sol";
import "../Libraries/Ownable.sol";
/*
The smart contract represents and stores obligations rules related to pods and resources.
The architecture of the market supposes that each initialized pod is owner of a 
*/ 
contract DTobligations is Ownable
{
    /*
    Reference to the DTindexing smart contract
    */ 
    DTindexing private dtIndexing;
    /*
    Default ObligationRules object associated with the pod.
    */
    ObligationRules private defaultPodObligation;
    /*
    Mapping that associates a pod's resource identifier with the related obligations rule.
    */
    mapping(int=>ObligationRules) resourcesObligation;
    /*
    Mapping that associates a pod's resource identifier with the related obligations rule.
    */
    modifier hasSpecificRules(int resourceId)
    {
        require(withSpecificRules(resourceId),"The resource has not specific obligaitons rules. Add specific rules, or changhe the default pod rules.");
        _;
    }
     /*
    Constructor of the smart contract
    */
    constructor(address dtInd,address podAddress)
    {
        dtIndexing=DTindexing(dtInd);
        transferOwnership(podAddress);
    }


    /*
    Modifier that checks if the temporal obligation value is valid.
    */
    modifier isValidTemporal(uint deadline)
    {
        uint d=1 days;
        require(deadline>d,"The temporal obligation must be at least 1 day");
        _;
    }


    /*
    Modifier that verifier if the given resource id is contained in the pod associated with the smart contract instance.
    */
    modifier isTheResourceCovered(int idResource)
    {
        DTindexing.Resource memory resource=dtIndexing.getResource(idResource);
        require(resource.owner==owner(),"The resource is not covered by this contract");
        _;
    }

    /*
    Function that returns the obligation rules associated with the resource of the given identifier.
    */
    function getObligationRules(int idResource) isTheResourceCovered(idResource) public view returns(ObligationRules memory)
    {
        if (resourcesObligation[idResource].exists)
        {
            return resourcesObligation[idResource];
        }
        return defaultPodObligation;
    }
    /*
    Function that returns the default ObligationRules object associated with the pod.
    */
    function getDefaultObligationRules() public view returns(ObligationRules memory)
    {
        return defaultPodObligation;
    }
    /*
    Function to set a default Access Counter obligation associated with the pod.
    */
    function addDefaultAccessCounterObligation(uint accessCounter)public 
    {
        defaultPodObligation.acObligation.exists=true;
        defaultPodObligation.acObligation.accessCounter=accessCounter;
    }

    
    /*
    Function that sets a default Temporal obligation associated with the pod.
    */
    function addDefaultTemporalObligation(uint temporalObligation)public isValidTemporal(temporalObligation) onlyOwner() {
        uint d=1 days;
        require(temporalObligation>d,"The temporal obligation must be at least 1 day");
        defaultPodObligation.temporalObligation.exists=true;
        defaultPodObligation.temporalObligation.usageDuration=temporalObligation;
    }
    /*
    Function that sets a default Country obligation associated with the pod.
    */
    function addDefaultCountryObligation(uint country)public onlyOwner(){
        defaultPodObligation.countryObligation.exists=true;
        defaultPodObligation.countryObligation.countryCode=country;
    }
    /*
    Function to set a default Domain obligation associated with the pod.
    */
    function adDefaultDomainObligation(DomainType domain) public onlyOwner()
    {
        defaultPodObligation.domainObligation.exists=true;
        defaultPodObligation.domainObligation.domain=domain;
    }
    /*
    Adds an Access Counter obligation for the given resource.
    */
    function addAccessCounterObligation(int idResource,uint accessCounter) isTheResourceCovered(idResource) public onlyOwner()  returns(ObligationRules memory){
        if (resourcesObligation[idResource].exists){
            resourcesObligation[idResource].acObligation=AccessCounterObligation(accessCounter,true);
        }
        else{
                resourcesObligation[idResource].exists=true;
                resourcesObligation[idResource].idResource=idResource;
                resourcesObligation[idResource].acObligation=AccessCounterObligation(accessCounter,true);
        }
        return resourcesObligation[idResource];  
        }
    /*
    Adds a Domain obligation for the given resource.
    */
    function addDomainObligation(int idResource,DomainType domain) public onlyOwner() isTheResourceCovered(idResource)  returns(ObligationRules memory){
        if (resourcesObligation[idResource].exists){
            resourcesObligation[idResource].domainObligation=DomainObligation(domain,true);
        }
        else{
                resourcesObligation[idResource].exists=true;
                resourcesObligation[idResource].idResource=idResource;
                resourcesObligation[idResource].domainObligation=DomainObligation(domain,true);
        }
        return resourcesObligation[idResource];  
    }
    /*
    Adds a Country obligation for the given resource.
    */
    function addCountryObligation(int idResource,uint country) public onlyOwner() isTheResourceCovered(idResource)  returns(ObligationRules memory){
            if (resourcesObligation[idResource].exists){
                resourcesObligation[idResource].countryObligation=CountryObligation(country,true);
            }
            else{
                    resourcesObligation[idResource].exists=true;
                    resourcesObligation[idResource].idResource=idResource;
                    resourcesObligation[idResource].countryObligation=CountryObligation(country,true);
            }
            return resourcesObligation[idResource];  
    }
    /*
    Adds a Temporal obligation for the given resource.
    */
    function addTemporalObligation(int idResource,uint deadline) onlyOwner() isTheResourceCovered(idResource) public isValidTemporal(deadline) returns(ObligationRules memory){

            if (resourcesObligation[idResource].exists){
                resourcesObligation[idResource].temporalObligation=TemporalObligation(deadline,true);
            }
            else{
                    resourcesObligation[idResource].exists=true;
                    resourcesObligation[idResource].idResource=idResource;
                    resourcesObligation[idResource].temporalObligation=TemporalObligation(deadline,true);
            }
            return resourcesObligation[idResource];  
    }
    /*
    Deactivates an Access Counter obligation for the given resource.
    */
    function removeAccessCounterObligation(int idResource) onlyOwner() isTheResourceCovered(idResource) public hasSpecificRules(idResource){

        resourcesObligation[idResource].acObligation.exists=false;
         resourcesObligation[idResource].acObligation.accessCounter=0;

    }
    /*
    Deactivates a Temporal obligation for the given resource.
    */
    function removeTemporalObligation(int idResource) isTheResourceCovered(idResource) onlyOwner() public hasSpecificRules(idResource){

        resourcesObligation[idResource].temporalObligation.exists=false;
        resourcesObligation[idResource].temporalObligation.usageDuration=0;
    }
    /*
    Deactivates a Domain obligation for the given resource.
    */
    function removeDomainObligation(int idResource) isTheResourceCovered(idResource) onlyOwner() public hasSpecificRules(idResource){

        resourcesObligation[idResource].domainObligation.exists=false;
        resourcesObligation[idResource].domainObligation.domain=DomainType.NULL;
    }
    /*
    Deactivates a Country obligation for the given resource.
    */
     function removeCountryObligation(int idResource) isTheResourceCovered(idResource) onlyOwner() public hasSpecificRules(idResource){

        resourcesObligation[idResource].countryObligation.exists=false;
        resourcesObligation[idResource].countryObligation.countryCode=0;
    }   
    /*
    Deactivates a default AccessCounter obligation associated with the pod.
    */
    function removeDefaultAccessCounterObligation() onlyOwner() public {
        defaultPodObligation.acObligation.exists=false;
        defaultPodObligation.acObligation.accessCounter=0;
    }
    /*
    Deactivates a Temporal obligation associated with the pod.
    */
    function removeDefaultTemporalObligation() onlyOwner() public {
        
        defaultPodObligation.temporalObligation.exists=false;
        defaultPodObligation.temporalObligation.usageDuration=0;
    }
    /*
    Deactivates a default Country obligation associated with the pod.
    */
    function removeDefaultCountryObligation() onlyOwner() public{
        defaultPodObligation.countryObligation.exists=false;
        defaultPodObligation.countryObligation.countryCode=0;
    }
    /*
    Deactivates a default Domain obligation associated with the pod.
    */    
    function removeDefaultDomainObligation() onlyOwner() public{
        defaultPodObligation.domainObligation.exists=false;
        defaultPodObligation.domainObligation.domain=DomainType.NULL;
    }
    /*
    Cheks if a given resource has specific obligation rules or inherits the default's pod rules.
    */
    function withSpecificRules(int idResource)view public returns(bool)
    {
        return resourcesObligation[idResource].exists;
    }
/*
Struct the represents obligation rules.
*/
struct ObligationRules{

    /*
    Identifier of the resource to which the rules refer. If it's related to the pod, a default value is set.
    */
    int idResource;
    /*
    AccessCounterObligation object.
    */
    AccessCounterObligation acObligation;
    /*
    CountryObligation object.
    */
    CountryObligation countryObligation;
    /*
    TemporalObligation object.
    */
    TemporalObligation temporalObligation;
    /*
    Domain Obligation object.
    */
    DomainObligation domainObligation;
    /*
    Flag that marks if the object exists.
    */
    bool exists;
}
/*
Struct that represents Access Counter obligations.
*/
struct AccessCounterObligation{
    /*
    Number of access that can be executed to a resource, when it is stored in the consumer's TEE.
    */
    uint accessCounter;
    bool exists;
}
/*
Struct that represents Country obligations.
*/
struct CountryObligation{
    /*
    Code of the country in which the resource can be accessed.
    */
    uint countryCode;
    bool exists;
}
/*
Struct that represents Temporal obligations.
*/
struct TemporalObligation{
    /*
    Unix duration of a resource in the consumer's TEE.
    */
    uint usageDuration;
    bool exists;
}
/*
Struct that represents Domain obligations.
*/
struct DomainObligation{
    /*
    Domain code that expresses the applications can use the resource.
    */
    DomainType domain;
    bool exists;
}

/*
Enum for domain types.
*/
enum DomainType{NULL,SOCIAL,FINANCIAL,MEDICAL}

}
