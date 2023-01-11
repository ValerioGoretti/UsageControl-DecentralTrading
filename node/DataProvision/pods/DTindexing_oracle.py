from web3 import Web3
from eth_account import Account
import secrets
from DTaddress_generator import DTaccount_generator
import web3
"""
Class that implements the communication mechanisms with the DTindexing smart contract.
"""
class DTindexing_oracle:

    """
    Class initializer.
    The function takes as input the DTindexing address and the private key of the pod.
    """
    def __init__(self, *args, **kw):
        self.indexing_address=args[0]
        self.contract_abi='[{"inputs":[{"internalType":"int256","name":"idResource","type":"int256"}],"name":"deactivateResource","outputs":[],"stateMutability":"nonpayable","type":"function"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"int256","name":"idPod","type":"int256"},{"indexed":false,"internalType":"address","name":"obligationAddress","type":"address"}],"name":"NewPod","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"int256","name":"idResource","type":"int256"}],"name":"NewResource","type":"event"},{"inputs":[{"internalType":"bytes","name":"newReference","type":"bytes"},{"internalType":"enumDTIndexing.PodType","name":"podType","type":"uint8"},{"internalType":"address","name":"podAddress","type":"address"}],"name":"registerPod","outputs":[{"internalType":"int256","name":"","type":"int256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"int256","name":"podId","type":"int256"},{"internalType":"bytes","name":"newReference","type":"bytes"},{"internalType":"uint256","name":"idSubscription","type":"uint256"}],"name":"registerResource","outputs":[{"internalType":"int256","name":"","type":"int256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"idSubscription","type":"uint256"}],"name":"getFinancialPods","outputs":[{"components":[{"internalType":"int256","name":"id","type":"int256"},{"internalType":"enumDTIndexing.PodType","name":"podType","type":"uint8"},{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"podAddress","type":"address"},{"internalType":"bytes","name":"baseUrl","type":"bytes"},{"internalType":"bool","name":"isActive","type":"bool"}],"internalType":"structDTIndexing.Pod[]","name":"","type":"tuple[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"idSubscription","type":"uint256"}],"name":"getMedicalPods","outputs":[{"components":[{"internalType":"int256","name":"id","type":"int256"},{"internalType":"enumDTIndexing.PodType","name":"podType","type":"uint8"},{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"podAddress","type":"address"},{"internalType":"bytes","name":"baseUrl","type":"bytes"},{"internalType":"bool","name":"isActive","type":"bool"}],"internalType":"structDTIndexing.Pod[]","name":"","type":"tuple[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"int256","name":"pod_id","type":"int256"},{"internalType":"uint256","name":"idSubscription","type":"uint256"}],"name":"getPodResources","outputs":[{"components":[{"internalType":"int256","name":"id","type":"int256"},{"internalType":"address","name":"owner","type":"address"},{"internalType":"bytes","name":"url","type":"bytes"},{"internalType":"int256","name":"podId","type":"int256"},{"internalType":"bool","name":"isActive","type":"bool"}],"internalType":"structDTIndexing.Resource[]","name":"","type":"tuple[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"int256","name":"idResource","type":"int256"}],"name":"getResource","outputs":[{"components":[{"internalType":"int256","name":"id","type":"int256"},{"internalType":"address","name":"owner","type":"address"},{"internalType":"bytes","name":"url","type":"bytes"},{"internalType":"int256","name":"podId","type":"int256"},{"internalType":"bool","name":"isActive","type":"bool"}],"internalType":"structDTIndexing.Resource","name":"","type":"tuple"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"idSubscription","type":"uint256"}],"name":"getSocialPods","outputs":[{"components":[{"internalType":"int256","name":"id","type":"int256"},{"internalType":"enumDTIndexing.PodType","name":"podType","type":"uint8"},{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"podAddress","type":"address"},{"internalType":"bytes","name":"baseUrl","type":"bytes"},{"internalType":"bool","name":"isActive","type":"bool"}],"internalType":"structDTIndexing.Pod[]","name":"","type":"tuple[]"}],"stateMutability":"view","type":"function"}]'
        self.private_key=args[1]
        self.account= Account.from_key(self.private_key)
        self.provider=Web3(Web3.HTTPProvider('HTTP://127.0.0.1:7545'))
        self.contract_instance = self.provider.eth.contract(address=self.indexing_address, abi=self.contract_abi)
    """
    Marks a given pod's resource as non-active.
    Generates a transaction and invokes the deactivateResource() method of the DTindexing smart contract.
    """       
    def deactivate_resource(self,resource_id):
        tx=self.contract_instance.functions.deactivateResource(resource_id).buildTransaction({'gasPrice': Web3.toWei(21, 'gwei'),'nonce': self.provider.eth.getTransactionCount(self.account.address)})
        signed_txn = self.provider.eth.account.sign_transaction(tx, private_key=self.private_key)
        tx=Web3.toHex(self.provider.eth.sendRawTransaction(signed_txn.rawTransaction))
        receipt=self.provider.eth.waitForTransactionReceipt(tx)
        if receipt:
            return True
        else:
            return False
    """
    Initialize a new resource and adds it to the pod.
    Generates a transaction and invokes the registerResource() method of the DTindexing smart contract.
    Waits the emission of a NewResource event to retrieve the resource id.
    """     
    def add_resource(self,reference,podId,subscription):
        tx=self.contract_instance.functions.registerResource(podId,reference,subscription).buildTransaction({'from': self.account.address,'gasPrice': Web3.toWei(21, 'gwei'),'nonce': self.provider.eth.getTransactionCount(self.account.address)})
        signed_txn = self.provider.eth.account.sign_transaction(tx, private_key=self.private_key)
        tx=Web3.toHex(self.provider.eth.sendRawTransaction(signed_txn.rawTransaction))
        retVal = self.provider.eth.waitForTransactionReceipt(tx)
        processed_receipt=self.contract_instance.events.NewResource().processReceipt(retVal)
        print(processed_receipt)
        id=processed_receipt[0]['args']['idResource']
        return id
    """
    Reads the resources of a given pod.
    Calls the getPodResources() method of the DTindexing smart contract.
    """         
    def get_resource_information(self,pod_id):
        contract_instance = self.provider.eth.contract(address=self.indexing_address, abi=self.contract_abi)
        return contract_instance.functions.getPodResources(pod_id,0).call()
    """
    Registers a new pod in the DecentralTrading market.
    Generates a transaction and invokes the registerPod() method of the DTindexing smart contract.
    Waits the emission of a NewPod event to retrieve the identifier of the new pod.
    """ 
    def register_Pod(self,pod_reference,pod_type,public_key_owner,private_key_owner):
        public_key_pod,private_key_pod=DTaccount_generator().generate_account()
        tx=self.contract_instance.functions.registerPod(pod_reference,pod_type,Web3.toChecksumAddress(public_key_pod)).buildTransaction({'gasPrice': Web3.toWei(21, 'gwei'),'nonce': self.provider.eth.getTransactionCount(public_key_owner)})
        signed_txn = self.provider.eth.account.sign_transaction(tx, private_key=private_key_owner)
        tx=Web3.toHex(self.provider.eth.sendRawTransaction(signed_txn.rawTransaction))
        retVal = self.provider.eth.waitForTransactionReceipt(tx)
        processed_receipt=self.contract_instance.events.NewPod().processReceipt(retVal)
        id=processed_receipt[0]['args']['idPod']
        obligation_address=processed_receipt[0]['args']['obligationAddress']
        return id,public_key_pod,private_key_pod,obligation_address
