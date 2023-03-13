// SPDX-License-Identifier: GPL-3.0
pragma solidity ^0.8.0;

abstract contract isUsingDTmonitoringOracle{
    
    function _callback(address consumer, int idMonitoring,int idResource, bytes memory response) virtual public;
}
contract DTmonitoringOracle
{
    isUsingDTmonitoringOracle public callback;
    function initializeMonitoring(address obligationsContract,int idMonitoring, int idResource) public
    {
      emit NewMonitoring(obligationsContract,idMonitoring,idResource);
    }
     function _callback(address obligationsContract,int idMonitoring, int idResource, bytes memory response)public {

        isUsingDTmonitoringOracle callback_contract=isUsingDTmonitoringOracle(obligationsContract);
        callback_contract._callback(msg.sender,idMonitoring,idResource,response);
    }

event NewMonitoring(address obligationsContract, int idMonitoring, int idResource);
}
