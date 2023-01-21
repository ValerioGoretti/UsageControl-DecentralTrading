// SPDX-License-Identifier: GPL-3.0
pragma solidity ^0.8.0;
//Interfaccia per il metodo di restituzione risposta dalla componente off-chain
abstract contract isUsingDTmonitoringOracle{
    
    function _callback(int idMonitoring,int idResource, bytes memory response) virtual public;
}
//smart contract che implementa la componenente on chain dell'oracolo pull based inbound
contract DTmonitoringOracle
{
     isUsingDTmonitoringOracle public callback;
    //funzione utilizzata dalle DApp per la sottomissione della risposta
    function newVerification(address obligationsContract,int idMonitoring, int idResource) public
    {
      emit NewMonitoring(obligationsContract,idMonitoring,idResource);
    }

    //funzione per la restituzione della risposta
     function _callback(address obligationsContract,int idMonitoring, int idResource, bytes memory response)public {

        isUsingDTmonitoringOracle callback_contract=isUsingDTmonitoringOracle(obligationsContract);
        callback_contract._callback(idMonitoring,idResource,response);
    }

    event NewMonitoring(address, int, int);
}