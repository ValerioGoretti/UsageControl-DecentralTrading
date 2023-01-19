from web3 import Web3

# Connect to the Ganache network
ganache_url = "http://127.0.0.1:8545"
w3 = Web3(Web3.HTTPProvider(ganache_url))

# Get the balance of an account
account = "0x4D561e53b23DF41c1659C01c4819475150f70bD7"
balance = w3.eth.getBalance(account)

# Convert the balance from wei to ether
balance_in_ether = w3.fromWei(balance, 'ether')
print(f"Balance of {account} is {balance_in_ether} ether")
