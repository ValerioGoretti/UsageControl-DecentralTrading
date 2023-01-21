from inspect import signature
from web3 import Web3
from datetime import datetime,timedelta,time
from datetime import datetime
import pytz
from hexbytes import HexBytes
from eth_account.messages import encode_defunct

"""
Rounds the given unix epoch of 5 minutes.
"""    
def rounded_to_the_last_5th_minute_epoch(unix_time):
    date_time = datetime.fromtimestamp(unix_time)
    now = date_time
    rounded = now - (now - datetime.min) % timedelta(minutes=5)
    return rounded.timestamp()
"""
Rounds the given unix epoch of 5 minutes.
""" 
def get_time_in_rome():
    rome_tz= pytz.timezone("Europe/Rome") 
    time_in_rome = datetime.now(rome_tz)
    return time_in_rome
"""
Build the message composed by the resource path, the :*:*: separator and the rounded unix time.
The message will be used to verify the given signature.
""" 
def encode_unsigned(resource,time):
    msg_to_hash=resource+":*:*:"+time
    msghash = encode_defunct(text=msg_to_hash)
    return msghash

"""
Wrapper function to authenticate the signature extracted from a HTTP request.
"""     
def authenticate(resource):
    time_in_rome=get_time_in_rome()
    rounded=rounded_to_the_last_5th_minute_epoch(int(time_in_rome.timestamp()))
    msg_hash=encode_unsigned(resource,str(rounded))
    w3 = Web3(Web3.HTTPProvider('http://localhost:8545'))
    signature = w3.eth.account.sign_message(msg_hash, "fb086b9dc76c5481cc8dc6f644d8e5814fa24dccbbc65d6262b78f3ae5a65170")
    

    print(signature)
authenticate("/test.py")