from web3 import Web3
from eth_account import Account
import secrets
class DTaccount_generator():

    def __init__(self, *args, **kw):
        self.w3=Web3(Web3.HTTPProvider('HTTP://127.0.0.1:7545'))
    
    def generate_account(self):
        return ("0x8d9F87A63C043FDCB7deBeAfFC193A387d113A14","da07cc12a14ff42b9859015d02cb526dc57639fabe03d85a0ed8d3cf4484772d")


