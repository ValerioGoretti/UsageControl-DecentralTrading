
from web3 import Web3
import time
import asyncio
async def log_loop(event_filter, poll_interval):
    while True:
        for NewMonitoring in event_filter.get_new_entries():
            handle_event(NewMonitoring)
        await asyncio.sleep(poll_interval)
def handle_event(event):
    print(Web3.toJSON(event))
    # and whatever

# Connect to a local Ethereum node
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))

# The address of the smart contract that you want to listen to
contract_address = '0xbFD0F6d8c51bD86ea0031fD1bB95E1ca810d64Aa'

# The ABI (Application Binary Interface) of the smart contract
contract_abi = '[{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"","type":"address"},{"indexed":false,"internalType":"int256","name":"","type":"int256"},{"indexed":false,"internalType":"int256","name":"","type":"int256"}],"name":"NewMonitoring","type":"event"},{"inputs":[{"internalType":"address","name":"obligationsContract","type":"address"},{"internalType":"int256","name":"idMonitoring","type":"int256"},{"internalType":"int256","name":"idResource","type":"int256"},{"internalType":"bytes","name":"response","type":"bytes"}],"name":"_callback","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"callback","outputs":[{"internalType":"contractisUsingDTmonitoringOracle","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"obligationsContract","type":"address"},{"internalType":"int256","name":"idMonitoring","type":"int256"},{"internalType":"int256","name":"idResource","type":"int256"}],"name":"initializeMonitoring","outputs":[],"stateMutability":"nonpayable","type":"function"}]'

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