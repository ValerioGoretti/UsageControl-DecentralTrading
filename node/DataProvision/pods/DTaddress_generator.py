from web3 import Web3
from eth_account import Account
import secrets
class DTaccount_generator():

    def __init__(self, *args, **kw):
        self.w3=Web3(Web3.HTTPProvider('HTTP://127.0.0.1:8545'))
    
    def generate_account(self):
        return ("0xe90D53F5ee94b726D1b1bf513Bfa03728795749D","fb086b9dc76c5481cc8dc6f644d8e5814fa24dccbbc65d6262b78f3ae5a65170")


