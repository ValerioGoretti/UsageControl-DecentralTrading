from os import access
from web3 import Web3
from eth_account import Account
import secrets
import asyncio
import web3
"""
Class that implements the communication mechanisms with the DTobligations smart contract.
"""
class DTobligation_oracle:
    """
    Class initializer.
    The function takes as input the address of the DTobligations smart contract and its ABI.
    """
    def __init__(self, *args, **kw):
        self.indexing_address=args[0]
        self.contract_abi='[{"inputs":[{"internalType":"address","name":"dtInd","type":"address"},{"internalType":"address","name":"podAddress","type":"address"},{"internalType":"address","name":"oracleAddress","type":"address"}],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"int256","name":"idMonitoring","type":"int256"},{"indexed":false,"internalType":"address","name":"consumer","type":"address"},{"indexed":false,"internalType":"bytes","name":"response","type":"bytes"}],"name":"NewMonitoringResponse","type":"event"},{"inputs":[{"internalType":"address","name":"consumer","type":"address"},{"internalType":"int256","name":"idMonitoring","type":"int256"},{"internalType":"int256","name":"idResource","type":"int256"},{"internalType":"bytes","name":"response","type":"bytes"}],"name":"_callback","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"enumDTobligations.DomainType","name":"domain","type":"uint8"}],"name":"adDefaultDomainObligation","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"int256","name":"idResource","type":"int256"},{"internalType":"uint256","name":"accessCounter","type":"uint256"}],"name":"addAccessCounterObligation","outputs":[{"components":[{"internalType":"int256","name":"idResource","type":"int256"},{"components":[{"internalType":"uint256","name":"accessCounter","type":"uint256"},{"internalType":"bool","name":"exists","type":"bool"}],"internalType":"structDTobligations.AccessCounterObligation","name":"acObligation","type":"tuple"},{"components":[{"internalType":"uint256","name":"countryCode","type":"uint256"},{"internalType":"bool","name":"exists","type":"bool"}],"internalType":"structDTobligations.CountryObligation","name":"countryObligation","type":"tuple"},{"components":[{"internalType":"uint256","name":"usageDuration","type":"uint256"},{"internalType":"bool","name":"exists","type":"bool"}],"internalType":"structDTobligations.TemporalObligation","name":"temporalObligation","type":"tuple"},{"components":[{"internalType":"enumDTobligations.DomainType","name":"domain","type":"uint8"},{"internalType":"bool","name":"exists","type":"bool"}],"internalType":"structDTobligations.DomainObligation","name":"domainObligation","type":"tuple"},{"internalType":"bool","name":"exists","type":"bool"}],"internalType":"structDTobligations.ObligationRules","name":"","type":"tuple"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"int256","name":"idResource","type":"int256"},{"internalType":"uint256","name":"country","type":"uint256"}],"name":"addCountryObligation","outputs":[{"components":[{"internalType":"int256","name":"idResource","type":"int256"},{"components":[{"internalType":"uint256","name":"accessCounter","type":"uint256"},{"internalType":"bool","name":"exists","type":"bool"}],"internalType":"structDTobligations.AccessCounterObligation","name":"acObligation","type":"tuple"},{"components":[{"internalType":"uint256","name":"countryCode","type":"uint256"},{"internalType":"bool","name":"exists","type":"bool"}],"internalType":"structDTobligations.CountryObligation","name":"countryObligation","type":"tuple"},{"components":[{"internalType":"uint256","name":"usageDuration","type":"uint256"},{"internalType":"bool","name":"exists","type":"bool"}],"internalType":"structDTobligations.TemporalObligation","name":"temporalObligation","type":"tuple"},{"components":[{"internalType":"enumDTobligations.DomainType","name":"domain","type":"uint8"},{"internalType":"bool","name":"exists","type":"bool"}],"internalType":"structDTobligations.DomainObligation","name":"domainObligation","type":"tuple"},{"internalType":"bool","name":"exists","type":"bool"}],"internalType":"structDTobligations.ObligationRules","name":"","type":"tuple"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"accessCounter","type":"uint256"}],"name":"addDefaultAccessCounterObligation","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"country","type":"uint256"}],"name":"addDefaultCountryObligation","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"temporalObligation","type":"uint256"}],"name":"addDefaultTemporalObligation","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"int256","name":"idResource","type":"int256"},{"internalType":"enumDTobligations.DomainType","name":"domain","type":"uint8"}],"name":"addDomainObligation","outputs":[{"components":[{"internalType":"int256","name":"idResource","type":"int256"},{"components":[{"internalType":"uint256","name":"accessCounter","type":"uint256"},{"internalType":"bool","name":"exists","type":"bool"}],"internalType":"structDTobligations.AccessCounterObligation","name":"acObligation","type":"tuple"},{"components":[{"internalType":"uint256","name":"countryCode","type":"uint256"},{"internalType":"bool","name":"exists","type":"bool"}],"internalType":"structDTobligations.CountryObligation","name":"countryObligation","type":"tuple"},{"components":[{"internalType":"uint256","name":"usageDuration","type":"uint256"},{"internalType":"bool","name":"exists","type":"bool"}],"internalType":"structDTobligations.TemporalObligation","name":"temporalObligation","type":"tuple"},{"components":[{"internalType":"enumDTobligations.DomainType","name":"domain","type":"uint8"},{"internalType":"bool","name":"exists","type":"bool"}],"internalType":"structDTobligations.DomainObligation","name":"domainObligation","type":"tuple"},{"internalType":"bool","name":"exists","type":"bool"}],"internalType":"structDTobligations.ObligationRules","name":"","type":"tuple"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"int256","name":"idResource","type":"int256"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"addTemporalObligation","outputs":[{"components":[{"internalType":"int256","name":"idResource","type":"int256"},{"components":[{"internalType":"uint256","name":"accessCounter","type":"uint256"},{"internalType":"bool","name":"exists","type":"bool"}],"internalType":"structDTobligations.AccessCounterObligation","name":"acObligation","type":"tuple"},{"components":[{"internalType":"uint256","name":"countryCode","type":"uint256"},{"internalType":"bool","name":"exists","type":"bool"}],"internalType":"structDTobligations.CountryObligation","name":"countryObligation","type":"tuple"},{"components":[{"internalType":"uint256","name":"usageDuration","type":"uint256"},{"internalType":"bool","name":"exists","type":"bool"}],"internalType":"structDTobligations.TemporalObligation","name":"temporalObligation","type":"tuple"},{"components":[{"internalType":"enumDTobligations.DomainType","name":"domain","type":"uint8"},{"internalType":"bool","name":"exists","type":"bool"}],"internalType":"structDTobligations.DomainObligation","name":"domainObligation","type":"tuple"},{"internalType":"bool","name":"exists","type":"bool"}],"internalType":"structDTobligations.ObligationRules","name":"","type":"tuple"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"getDefaultObligationRules","outputs":[{"components":[{"internalType":"int256","name":"idResource","type":"int256"},{"components":[{"internalType":"uint256","name":"accessCounter","type":"uint256"},{"internalType":"bool","name":"exists","type":"bool"}],"internalType":"structDTobligations.AccessCounterObligation","name":"acObligation","type":"tuple"},{"components":[{"internalType":"uint256","name":"countryCode","type":"uint256"},{"internalType":"bool","name":"exists","type":"bool"}],"internalType":"structDTobligations.CountryObligation","name":"countryObligation","type":"tuple"},{"components":[{"internalType":"uint256","name":"usageDuration","type":"uint256"},{"internalType":"bool","name":"exists","type":"bool"}],"internalType":"structDTobligations.TemporalObligation","name":"temporalObligation","type":"tuple"},{"components":[{"internalType":"enumDTobligations.DomainType","name":"domain","type":"uint8"},{"internalType":"bool","name":"exists","type":"bool"}],"internalType":"structDTobligations.DomainObligation","name":"domainObligation","type":"tuple"},{"internalType":"bool","name":"exists","type":"bool"}],"internalType":"structDTobligations.ObligationRules","name":"","type":"tuple"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"int256","name":"idResource","type":"int256"}],"name":"getObligationRules","outputs":[{"components":[{"internalType":"int256","name":"idResource","type":"int256"},{"components":[{"internalType":"uint256","name":"accessCounter","type":"uint256"},{"internalType":"bool","name":"exists","type":"bool"}],"internalType":"structDTobligations.AccessCounterObligation","name":"acObligation","type":"tuple"},{"components":[{"internalType":"uint256","name":"countryCode","type":"uint256"},{"internalType":"bool","name":"exists","type":"bool"}],"internalType":"structDTobligations.CountryObligation","name":"countryObligation","type":"tuple"},{"components":[{"internalType":"uint256","name":"usageDuration","type":"uint256"},{"internalType":"bool","name":"exists","type":"bool"}],"internalType":"structDTobligations.TemporalObligation","name":"temporalObligation","type":"tuple"},{"components":[{"internalType":"enumDTobligations.DomainType","name":"domain","type":"uint8"},{"internalType":"bool","name":"exists","type":"bool"}],"internalType":"structDTobligations.DomainObligation","name":"domainObligation","type":"tuple"},{"internalType":"bool","name":"exists","type":"bool"}],"internalType":"structDTobligations.ObligationRules","name":"","type":"tuple"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"int256","name":"idResource","type":"int256"}],"name":"monitor_compliance","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"int256","name":"idResource","type":"int256"}],"name":"removeAccessCounterObligation","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"int256","name":"idResource","type":"int256"}],"name":"removeCountryObligation","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"removeDefaultAccessCounterObligation","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"removeDefaultCountryObligation","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"removeDefaultDomainObligation","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"removeDefaultTemporalObligation","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"int256","name":"idResource","type":"int256"}],"name":"removeDomainObligation","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"int256","name":"idResource","type":"int256"}],"name":"removeTemporalObligation","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"int256","name":"idResource","type":"int256"}],"name":"withSpecificRules","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"}]'
        self.private_key=args[1]
        self.account= Account.from_key(self.private_key)
        self.provider=Web3(Web3.HTTPProvider('HTTP://127.0.0.1:8545'))
        self.contract_instance = self.provider.eth.contract(address=self.indexing_address, abi=self.contract_abi)
        self.STOP_MONITORING=False
    """
    Sets an access counter obligation valid for the whole pod.
    Invokes the addDefaultAccessCounterObligation() method of the DTobligation smart contract.
    """        
    def set_default_access_counter_obligation(self,access_counter):
        tx=self.contract_instance.functions.addDefaultAccessCounterObligation(access_counter).buildTransaction({'gasPrice': Web3.toWei(21, 'gwei'),'nonce': self.provider.eth.getTransactionCount(self.account.address)})
        signed_txn = self.provider.eth.account.sign_transaction(tx, private_key=self.private_key)
        tx=Web3.toHex(self.provider.eth.sendRawTransaction(signed_txn.rawTransaction))
        print(self.provider.eth.waitForTransactionReceipt(tx))
        
    """
    Sets a temporal obligation valid for the whole pod.
    Invokes the addDefaultTemporalObligation() method of the DTobligation smart contract.
    """
    def set_default_temporal_obligation(self,temporalObligation):
        tx=self.contract_instance.functions.addDefaultTemporalObligation(temporalObligation).buildTransaction({'gasPrice': Web3.toWei(21, 'gwei'),'nonce': self.provider.eth.getTransactionCount(self.account.address)})
        signed_txn = self.provider.eth.account.sign_transaction(tx, private_key=self.private_key)
        tx=Web3.toHex(self.provider.eth.sendRawTransaction(signed_txn.rawTransaction))
        print(self.provider.eth.waitForTransactionReceipt(tx))
    """
    Remove an access counter obligation valid for the whole pod.
    Invokes the removeDefaultAccessCounterObligation() method of the DTobligation smart contract.
    """
    def deactivate_default_access_counter_obligation(self):
        tx=self.contract_instance.functions.removeDefaultAccessCounterObligation().buildTransaction({'gasPrice': Web3.toWei(21, 'gwei'),'nonce': self.provider.eth.getTransactionCount(self.account.address)})
        signed_txn = self.provider.eth.account.sign_transaction(tx, private_key=self.private_key)
        tx=Web3.toHex(self.provider.eth.sendRawTransaction(signed_txn.rawTransaction))
        print(self.provider.eth.waitForTransactionReceipt(tx))
    """
    Remove a temporal obligation valid for the whole pod.
    Invokes the removeDefaultTemporalObligation() method of the DTobligation smart contract.
    """
    def deactivate_default_temporal_obligation(self):
        tx=self.contract_instance.functions.removeDefaultTemporalObligation().buildTransaction({'gasPrice': Web3.toWei(21, 'gwei'),'nonce': self.provider.eth.getTransactionCount(self.account.address)})
        signed_txn = self.provider.eth.account.sign_transaction(tx, private_key=self.private_key)
        tx=Web3.toHex(self.provider.eth.sendRawTransaction(signed_txn.rawTransaction))
        print(self.provider.eth.waitForTransactionReceipt(tx))
    """
    Sets an access counter obligation associated with a specific resource.
    Invokes the addAccessCounterObligation() method of the DTobligation smart contract.
    """        
    def set_access_counter_obligation(self,id,access_counter):
        tx=self.contract_instance.functions.addAccessCounterObligation(id,access_counter).buildTransaction({'gasPrice': Web3.toWei(21, 'gwei'),'nonce': self.provider.eth.getTransactionCount(self.account.address)})
        signed_txn = self.provider.eth.account.sign_transaction(tx, private_key=self.private_key)
        tx=Web3.toHex(self.provider.eth.sendRawTransaction(signed_txn.rawTransaction))
        print(self.provider.eth.waitForTransactionReceipt(tx))
    """
    Sets an access counter obligation associated with a specific resource.
    Invokes the addTemporalObligation() method of the DTobligation smart contract.
    """ 
    def set_temporal_obligation(self,id,temporalObligation):
        tx=self.contract_instance.functions.addTemporalObligation(id,temporalObligation).buildTransaction({'gasPrice': Web3.toWei(21, 'gwei'),'nonce': self.provider.eth.getTransactionCount(self.account.address)})
        signed_txn = self.provider.eth.account.sign_transaction(tx, private_key=self.private_key)
        tx=Web3.toHex(self.provider.eth.sendRawTransaction(signed_txn.rawTransaction))
        print(self.provider.eth.waitForTransactionReceipt(tx))
    """
    Deactivate an access counter obligation associated with a specific resource.
    Invokes the removeAccessCounterObligation() method of the DTobligation smart contract.
    """ 
    def deactivate_access_counter_obligation(self,id):
        tx=self.contract_instance.functions.removeAccessCounterObligation(id).buildTransaction({'gasPrice': Web3.toWei(21, 'gwei'),'nonce': self.provider.eth.getTransactionCount(self.account.address)})
        signed_txn = self.provider.eth.account.sign_transaction(tx, private_key=self.private_key)
        tx=Web3.toHex(self.provider.eth.sendRawTransaction(signed_txn.rawTransaction))
        print(self.provider.eth.waitForTransactionReceipt(tx))
    """
    Deactivate a temporal obligation associated with a specific resource.
    Invokes the removeTemporalObligation() method of the DTobligation smart contract.
    """ 
    def deactivate_temporal_obligation(self,id):
        tx=self.contract_instance.functions.removeTemporalObligation(id).buildTransaction({'gasPrice': Web3.toWei(21, 'gwei'),'nonce': self.provider.eth.getTransactionCount(self.account.address)})
        signed_txn = self.provider.eth.account.sign_transaction(tx, private_key=self.private_key)
        tx=Web3.toHex(self.provider.eth.sendRawTransaction(signed_txn.rawTransaction))
        print(self.provider.eth.waitForTransactionReceipt(tx))
    """
    Sets a country obligation for the whole pod.
    Invokes the addDefaultCountryObligation() method of the DTobligation smart contract.
    """ 
    def set_default_country_obligation(self,country):
        tx=self.contract_instance.functions.addDefaultCountryObligation(country).buildTransaction({'gasPrice': Web3.toWei(21, 'gwei'),'nonce': self.provider.eth.getTransactionCount(self.account.address)})
        signed_txn = self.provider.eth.account.sign_transaction(tx, private_key=self.private_key)
        tx=Web3.toHex(self.provider.eth.sendRawTransaction(signed_txn.rawTransaction))
        print(self.provider.eth.waitForTransactionReceipt(tx))        
    """
    Sets a country obligation associated with a specific resource.
    Invokes the addCountryObligation() method of the DTobligation smart contract.
    """ 
    def set_country_obligation(self,id,country):
        tx=self.contract_instance.functions.addCountryObligation(id,country).buildTransaction({'gasPrice': Web3.toWei(21, 'gwei'),'nonce': self.provider.eth.getTransactionCount(self.account.address)})
        signed_txn = self.provider.eth.account.sign_transaction(tx, private_key=self.private_key)
        tx=Web3.toHex(self.provider.eth.sendRawTransaction(signed_txn.rawTransaction))
        print(self.provider.eth.waitForTransactionReceipt(tx))    
    """
    Sets a domain obligation associated with a specific resource.
    Invokes the addDomainObligation() method of the DTobligation smart contract.
    """     
    def set_domain_obligation(self,id,domain):
        tx=self.contract_instance.functions.addDomainObligation(id,domain).buildTransaction({'gasPrice': Web3.toWei(21, 'gwei'),'nonce': self.provider.eth.getTransactionCount(self.account.address)})
        signed_txn = self.provider.eth.account.sign_transaction(tx, private_key=self.private_key)
        tx=Web3.toHex(self.provider.eth.sendRawTransaction(signed_txn.rawTransaction))
        print(self.provider.eth.waitForTransactionReceipt(tx))
    """
    Sets a domain obligation for the whole pod.
    Invokes the addDefaultDomainObligation() method of the DTobligation smart contract.
    """ 
    def set_default_domain_obligation(self,domain):
        tx=self.contract_instance.functions.adDefaultDomainObligation(domain).buildTransaction({'gasPrice': Web3.toWei(21, 'gwei'),'nonce': self.provider.eth.getTransactionCount(self.account.address)})
        signed_txn = self.provider.eth.account.sign_transaction(tx, private_key=self.private_key)
        tx=Web3.toHex(self.provider.eth.sendRawTransaction(signed_txn.rawTransaction))
        print(self.provider.eth.waitForTransactionReceipt(tx))
    """
    Deactivate a domain obligation associated with a specific resource.
    Invokes the removeDomainObligation() method of the DTobligation smart contract.
    """     
    def deactivate_domain_obligation(self,id):
        tx=self.contract_instance.functions.removeDomainObligation(id).buildTransaction({'gasPrice': Web3.toWei(21, 'gwei'),'nonce': self.provider.eth.getTransactionCount(self.account.address)})
        signed_txn = self.provider.eth.account.sign_transaction(tx, private_key=self.private_key)
        tx=Web3.toHex(self.provider.eth.sendRawTransaction(signed_txn.rawTransaction))
        print(self.provider.eth.waitForTransactionReceipt(tx))
    """
    Deactivate a domain obligation for the whole pod.
    Invokes the removeDefaultDomainObligation() method of the DTobligation smart contract.
    """     
    def deactivate_default_domain_obligation(self):
        tx=self.contract_instance.functions.removeDefaultDomainObligation().buildTransaction({'gasPrice': Web3.toWei(21, 'gwei'),'nonce': self.provider.eth.getTransactionCount(self.account.address)})
        signed_txn = self.provider.eth.account.sign_transaction(tx, private_key=self.private_key)
        tx=Web3.toHex(self.provider.eth.sendRawTransaction(signed_txn.rawTransaction))
        print(self.provider.eth.waitForTransactionReceipt(tx))
    """
    Deactivate a country obligation for the whole pod.
    Invokes the removeDefaultCountryObligation() method of the DTobligation smart contract.
    """
    def deactivate_default_country_obligation(self):
        tx=self.contract_instance.functions.removeDefaultCountryObligation().buildTransaction({'gasPrice': Web3.toWei(21, 'gwei'),'nonce': self.provider.eth.getTransactionCount(self.account.address)})
        signed_txn = self.provider.eth.account.sign_transaction(tx, private_key=self.private_key)
        tx=Web3.toHex(self.provider.eth.sendRawTransaction(signed_txn.rawTransaction))
        print(self.provider.eth.waitForTransactionReceipt(tx))
    """
    Deactivate a country obligation associated with a specific resource.
    Invokes the removeCountryObligation() method of the DTobligation smart contract.
    """
    def deactivate_country_obligation(self,id):
        tx=self.contract_instance.functions.removeCountryObligation(id).buildTransaction({'gasPrice': Web3.toWei(21, 'gwei'),'nonce': self.provider.eth.getTransactionCount(self.account.address)})
        signed_txn = self.provider.eth.account.sign_transaction(tx, private_key=self.private_key)
        tx=Web3.toHex(self.provider.eth.sendRawTransaction(signed_txn.rawTransaction))
        print(self.provider.eth.waitForTransactionReceipt(tx))

    def listen_monitoring_response(self):
        event_name= 'NewMonitoringResponse'
        events = self.contract_instance.events.NewMonitoringResponse.createFilter(fromBlock='latest')
        last_block = self.provider.eth.blockNumber
        #loop = asyncio.get_event_loop()
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            loop.run_until_complete(
                asyncio.gather(self.log_loop(events, 2)))
        finally:
            loop.close()
    def stop_monitoring(self):
        self.STOP_MONITORING=True
    async def log_loop(self,event_filter, poll_interval):
        print("Listening for monitoring response from contract: {0}".format(self.indexing_address))
        while not self.STOP_MONITORING:
            for NewMonitoringResponse in event_filter.get_new_entries():
                self.handle_event(NewMonitoringResponse)
            await asyncio.sleep(poll_interval)
    def handle_event(self,event):
        print("Response Receipt - Id Monitoring: {0}, Consumer: {1}, Response: {2}".format(event.args['idMonitoring'],event.args['consumer'],event.args['response']))