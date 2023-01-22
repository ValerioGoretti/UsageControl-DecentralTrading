"""
from web3 import Web3
import time
import asyncio
async def log_loop(event_filter, poll_interval):
    while True:
        for NewMonitoring in event_filter.get_new_entries():
            handle_event(NewMonitoring)
        await asyncio.sleep(poll_interval)
def handle_event(event):
    print(event.args['obligationsContract'])
    print(event.args['idMonitoring'])
    print(event.args['idResource'])


# Connect to a local Ethereum node
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))

# The address of the smart contract that you want to listen to
contract_address = '0xF919001317631f2602d92DCc609c3c10Bd6cD698'

# The ABI (Application Binary Interface) of the smart contract
contract_abi = '[{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"obligationsContract","type":"address"},{"indexed":false,"internalType":"int256","name":"idMonitoring","type":"int256"},{"indexed":false,"internalType":"int256","name":"idResource","type":"int256"}],"name":"NewMonitoring","type":"event"},{"inputs":[{"internalType":"address","name":"obligationsContract","type":"address"},{"internalType":"int256","name":"idMonitoring","type":"int256"},{"internalType":"int256","name":"idResource","type":"int256"},{"internalType":"bytes","name":"response","type":"bytes"}],"name":"_callback","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"callback","outputs":[{"internalType":"contractisUsingDTmonitoringOracle","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"obligationsContract","type":"address"},{"internalType":"int256","name":"idMonitoring","type":"int256"},{"internalType":"int256","name":"idResource","type":"int256"}],"name":"initializeMonitoring","outputs":[],"stateMutability":"nonpayable","type":"function"}]'

# Create a contract object
contract = w3.eth.contract(address=contract_address, abi=contract_abi)

# The name of the event you want to listen to
from eth_abi import encode_single
event_name= 'NewMonitoring'


# Listen for events
events = contract.events.NewMonitoring.createFilter(fromBlock='latest')



# The block number of the last processed event
last_block = w3.eth.blockNumber

loop = asyncio.get_event_loop()
try:
    loop.run_until_complete(
        asyncio.gather(
            log_loop(events, 2)))
            # log_loop(block_filter, 2),
            # log_loop(tx_filter, 2)))
finally:
    # close loop to free up system resources
    loop.close()
"""
from web3 import Web3
from eth_account import Account
import secrets
import asyncio
import web3
"""
Class that implements the communication mechanisms with the DTindexing smart contract.
"""
class DTmonitoring_oracle:

    """
    Class initializer.
    The function takes as input the DTindexing address and the private key of the pod.
    """
    def __init__(self, *args, **kw):
        self.monitoring_oracle_address=args[0]
        self.contract_abi='[{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"obligationsContract","type":"address"},{"indexed":false,"internalType":"int256","name":"idMonitoring","type":"int256"},{"indexed":false,"internalType":"int256","name":"idResource","type":"int256"}],"name":"NewMonitoring","type":"event"},{"inputs":[{"internalType":"address","name":"obligationsContract","type":"address"},{"internalType":"int256","name":"idMonitoring","type":"int256"},{"internalType":"int256","name":"idResource","type":"int256"},{"internalType":"bytes","name":"response","type":"bytes"}],"name":"_callback","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"callback","outputs":[{"internalType":"contractisUsingDTmonitoringOracle","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"obligationsContract","type":"address"},{"internalType":"int256","name":"idMonitoring","type":"int256"},{"internalType":"int256","name":"idResource","type":"int256"}],"name":"initializeMonitoring","outputs":[],"stateMutability":"nonpayable","type":"function"}]'
        self.private_key=args[1]
        self.account= Account.from_key(self.private_key)
        self.provider=Web3(Web3.HTTPProvider('HTTP://127.0.0.1:8545'))
        self.contract_instance = self.provider.eth.contract(address=self.monitoring_oracle_address, abi=self.contract_abi)
    
    
    def listen_monitoring_requests(self):
        event_name= 'NewMonitoring'
        events = self.contract_instance.events.NewMonitoring.createFilter(fromBlock='latest')
        last_block = self.provider.eth.blockNumber
        loop = asyncio.get_event_loop()
        try:
            loop.run_until_complete(
                asyncio.gather(self.log_loop(events, 2)))
        finally:
            loop.close()
    async def log_loop(self,event_filter, poll_interval):
        while True:
            for NewMonitoring in event_filter.get_new_entries():
                self.handle_event(NewMonitoring)
            await asyncio.sleep(poll_interval)
    def handle_event(self,event):
        print(event.args['obligationsContract'])
        print(event.args['idMonitoring'])
        print(event.args['idResource'])
    def send_monitoring_response(self,obligationsContract,idMonitoring,idResource,response):
        tx=self.contract_instance.functions._callback(Web3.toChecksumAddress(obligationsContract),idMonitoring,idResource,response).buildTransaction({'gasPrice': Web3.toWei(21, 'gwei'),'nonce': self.provider.eth.getTransactionCount(self.provider.eth.account.privateKeyToAccount(self.private_key).address)})
        signed_txn = self.provider.eth.account.sign_transaction(tx, private_key=self.private_key)
        tx=Web3.toHex(self.provider.eth.sendRawTransaction(signed_txn.rawTransaction))
        retVal = self.provider.eth.waitForTransactionReceipt(tx)
       # print(retVal)
        obligation_contract=self.provider.eth.contract(address=obligationsContract, abi='[{"anonymous":false,"inputs":[{"indexed":false,"internalType":"int256","name":"idMonitoring","type":"int256"},{"indexed":false,"internalType":"address","name":"consumer","type":"address"},{"indexed":false,"internalType":"bytes","name":"response","type":"bytes"}],"name":"NewMonitoringResponse","type":"event"},{"inputs":[{"internalType":"int256","name":"idMonitoring","type":"int256"},{"internalType":"int256","name":"idResource","type":"int256"},{"internalType":"bytes","name":"response","type":"bytes"}],"name":"_callback","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"int256","name":"idResource","type":"int256"},{"internalType":"uint256","name":"accessCounter","type":"uint256"}],"name":"addAccessCounterObligation","outputs":[{"components":[{"internalType":"int256","name":"idResource","type":"int256"},{"components":[{"internalType":"uint256","name":"accessCounter","type":"uint256"},{"internalType":"bool","name":"exists","type":"bool"}],"internalType":"structDTobligations.AccessCounterObligation","name":"acObligation","type":"tuple"},{"components":[{"internalType":"uint256","name":"countryCode","type":"uint256"},{"internalType":"bool","name":"exists","type":"bool"}],"internalType":"structDTobligations.CountryObligation","name":"countryObligation","type":"tuple"},{"components":[{"internalType":"uint256","name":"usageDuration","type":"uint256"},{"internalType":"bool","name":"exists","type":"bool"}],"internalType":"structDTobligations.TemporalObligation","name":"temporalObligation","type":"tuple"},{"components":[{"internalType":"enumDTobligations.DomainType","name":"domain","type":"uint8"},{"internalType":"bool","name":"exists","type":"bool"}],"internalType":"structDTobligations.DomainObligation","name":"domainObligation","type":"tuple"},{"internalType":"bool","name":"exists","type":"bool"}],"internalType":"structDTobligations.ObligationRules","name":"","type":"tuple"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"int256","name":"idResource","type":"int256"},{"internalType":"uint256","name":"country","type":"uint256"}],"name":"addCountryObligation","outputs":[{"components":[{"internalType":"int256","name":"idResource","type":"int256"},{"components":[{"internalType":"uint256","name":"accessCounter","type":"uint256"},{"internalType":"bool","name":"exists","type":"bool"}],"internalType":"structDTobligations.AccessCounterObligation","name":"acObligation","type":"tuple"},{"components":[{"internalType":"uint256","name":"countryCode","type":"uint256"},{"internalType":"bool","name":"exists","type":"bool"}],"internalType":"structDTobligations.CountryObligation","name":"countryObligation","type":"tuple"},{"components":[{"internalType":"uint256","name":"usageDuration","type":"uint256"},{"internalType":"bool","name":"exists","type":"bool"}],"internalType":"structDTobligations.TemporalObligation","name":"temporalObligation","type":"tuple"},{"components":[{"internalType":"enumDTobligations.DomainType","name":"domain","type":"uint8"},{"internalType":"bool","name":"exists","type":"bool"}],"internalType":"structDTobligations.DomainObligation","name":"domainObligation","type":"tuple"},{"internalType":"bool","name":"exists","type":"bool"}],"internalType":"structDTobligations.ObligationRules","name":"","type":"tuple"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"accessCounter","type":"uint256"}],"name":"addDefaultAccessCounterObligation","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"country","type":"uint256"}],"name":"addDefaultCountryObligation","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"temporalObligation","type":"uint256"}],"name":"addDefaultTemporalObligation","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"int256","name":"idResource","type":"int256"},{"internalType":"enumDTobligations.DomainType","name":"domain","type":"uint8"}],"name":"addDomainObligation","outputs":[{"components":[{"internalType":"int256","name":"idResource","type":"int256"},{"components":[{"internalType":"uint256","name":"accessCounter","type":"uint256"},{"internalType":"bool","name":"exists","type":"bool"}],"internalType":"structDTobligations.AccessCounterObligation","name":"acObligation","type":"tuple"},{"components":[{"internalType":"uint256","name":"countryCode","type":"uint256"},{"internalType":"bool","name":"exists","type":"bool"}],"internalType":"structDTobligations.CountryObligation","name":"countryObligation","type":"tuple"},{"components":[{"internalType":"uint256","name":"usageDuration","type":"uint256"},{"internalType":"bool","name":"exists","type":"bool"}],"internalType":"structDTobligations.TemporalObligation","name":"temporalObligation","type":"tuple"},{"components":[{"internalType":"enumDTobligations.DomainType","name":"domain","type":"uint8"},{"internalType":"bool","name":"exists","type":"bool"}],"internalType":"structDTobligations.DomainObligation","name":"domainObligation","type":"tuple"},{"internalType":"bool","name":"exists","type":"bool"}],"internalType":"structDTobligations.ObligationRules","name":"","type":"tuple"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"enumDTobligations.DomainType","name":"domain","type":"uint8"}],"name":"adDefaultDomainObligation","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"int256","name":"idResource","type":"int256"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"addTemporalObligation","outputs":[{"components":[{"internalType":"int256","name":"idResource","type":"int256"},{"components":[{"internalType":"uint256","name":"accessCounter","type":"uint256"},{"internalType":"bool","name":"exists","type":"bool"}],"internalType":"structDTobligations.AccessCounterObligation","name":"acObligation","type":"tuple"},{"components":[{"internalType":"uint256","name":"countryCode","type":"uint256"},{"internalType":"bool","name":"exists","type":"bool"}],"internalType":"structDTobligations.CountryObligation","name":"countryObligation","type":"tuple"},{"components":[{"internalType":"uint256","name":"usageDuration","type":"uint256"},{"internalType":"bool","name":"exists","type":"bool"}],"internalType":"structDTobligations.TemporalObligation","name":"temporalObligation","type":"tuple"},{"components":[{"internalType":"enumDTobligations.DomainType","name":"domain","type":"uint8"},{"internalType":"bool","name":"exists","type":"bool"}],"internalType":"structDTobligations.DomainObligation","name":"domainObligation","type":"tuple"},{"internalType":"bool","name":"exists","type":"bool"}],"internalType":"structDTobligations.ObligationRules","name":"","type":"tuple"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"int256","name":"idResource","type":"int256"}],"name":"monitor_compliance","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"int256","name":"idResource","type":"int256"}],"name":"removeAccessCounterObligation","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"int256","name":"idResource","type":"int256"}],"name":"removeCountryObligation","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"removeDefaultAccessCounterObligation","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"removeDefaultCountryObligation","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"removeDefaultDomainObligation","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"removeDefaultTemporalObligation","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"int256","name":"idResource","type":"int256"}],"name":"removeDomainObligation","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"int256","name":"idResource","type":"int256"}],"name":"removeTemporalObligation","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"dtInd","type":"address"},{"internalType":"address","name":"podAddress","type":"address"},{"internalType":"address","name":"oracleAddress","type":"address"}],"stateMutability":"nonpayable","type":"constructor"},{"inputs":[],"name":"getDefaultObligationRules","outputs":[{"components":[{"internalType":"int256","name":"idResource","type":"int256"},{"components":[{"internalType":"uint256","name":"accessCounter","type":"uint256"},{"internalType":"bool","name":"exists","type":"bool"}],"internalType":"structDTobligations.AccessCounterObligation","name":"acObligation","type":"tuple"},{"components":[{"internalType":"uint256","name":"countryCode","type":"uint256"},{"internalType":"bool","name":"exists","type":"bool"}],"internalType":"structDTobligations.CountryObligation","name":"countryObligation","type":"tuple"},{"components":[{"internalType":"uint256","name":"usageDuration","type":"uint256"},{"internalType":"bool","name":"exists","type":"bool"}],"internalType":"structDTobligations.TemporalObligation","name":"temporalObligation","type":"tuple"},{"components":[{"internalType":"enumDTobligations.DomainType","name":"domain","type":"uint8"},{"internalType":"bool","name":"exists","type":"bool"}],"internalType":"structDTobligations.DomainObligation","name":"domainObligation","type":"tuple"},{"internalType":"bool","name":"exists","type":"bool"}],"internalType":"structDTobligations.ObligationRules","name":"","type":"tuple"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"int256","name":"idResource","type":"int256"}],"name":"getObligationRules","outputs":[{"components":[{"internalType":"int256","name":"idResource","type":"int256"},{"components":[{"internalType":"uint256","name":"accessCounter","type":"uint256"},{"internalType":"bool","name":"exists","type":"bool"}],"internalType":"structDTobligations.AccessCounterObligation","name":"acObligation","type":"tuple"},{"components":[{"internalType":"uint256","name":"countryCode","type":"uint256"},{"internalType":"bool","name":"exists","type":"bool"}],"internalType":"structDTobligations.CountryObligation","name":"countryObligation","type":"tuple"},{"components":[{"internalType":"uint256","name":"usageDuration","type":"uint256"},{"internalType":"bool","name":"exists","type":"bool"}],"internalType":"structDTobligations.TemporalObligation","name":"temporalObligation","type":"tuple"},{"components":[{"internalType":"enumDTobligations.DomainType","name":"domain","type":"uint8"},{"internalType":"bool","name":"exists","type":"bool"}],"internalType":"structDTobligations.DomainObligation","name":"domainObligation","type":"tuple"},{"internalType":"bool","name":"exists","type":"bool"}],"internalType":"structDTobligations.ObligationRules","name":"","type":"tuple"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"int256","name":"idResource","type":"int256"}],"name":"withSpecificRules","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"}]')
        processed_receipt=obligation_contract.events.NewMonitoringResponse().processReceipt(retVal)
        print(processed_receipt[0].args['idMonitoring'])
        print(processed_receipt[0].args['consumer'])
        print(processed_receipt[0].args['response'])
a=DTmonitoring_oracle("0xC7a06c66ED829FBdb27F547Fa47aE63B993766Bb","fb086b9dc76c5481cc8dc6f644d8e5814fa24dccbbc65d6262b78f3ae5a65170")
a.send_monitoring_response("0x1eBADcBA009D3C9f685649ceD4eeF791daf5D371",0,0,bytes("ciao", 'utf-8'))