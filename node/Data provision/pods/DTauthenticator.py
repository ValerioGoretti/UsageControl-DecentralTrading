from inspect import signature
from web3 import Web3
from datetime import datetime,timedelta,time
from datetime import datetime
import pytz
from hexbytes import HexBytes
from eth_account.messages import encode_defunct
"""
Class that implements the functions to authenticate HTTP requests for the resources.
"""
class DTauthenticator():
    """
    Class initializer.
    """
    def __init__(self, *args, **kw):
        self.w3=Web3(Web3.HTTPProvider('HTTP://127.0.0.1:7545'))
    """
    Rounds the given unix epoch of 5 minutes.
    """    
    def rounded_to_the_last_5th_minute_epoch(self,unix_time):
        date_time = datetime.fromtimestamp(unix_time)
        now = date_time
        rounded = now - (now - datetime.min) % timedelta(minutes=5)
        return rounded.timestamp()
    """
    Rounds the given unix epoch of 5 minutes.
    """ 
    def get_time_in_rome(self):
        rome_tz= pytz.timezone("Europe/Rome") 
        time_in_rome = datetime.now(rome_tz)
        return time_in_rome
    """
    Build the message composed by the resource path, the :*:*: separator and the rounded unix time.
    The message will be used to verify the given signature.
    """ 
    def encode_unsigned(self,resource,time):
        msg_to_hash=resource+":*:*:"+time
        msghash = encode_defunct(text=msg_to_hash)
        return msghash
    """
    Verifies if the signature extracted from the HTTP request has been signed by the claimed identity's credentrials.
    Makes use of the unsigned authentication message build according to the requested resource and the acutal rounded unix epoch.
    """    
    def authenticate_signature(self,signature,msg_hash,claim):
        return claim==self.w3.eth.account.recover_message(msg_hash, signature=signature)
    """
    Wrapper function to authenticate the signature extracted from a HTTP request.
    """     
    def authenticate(self,resource,signature,claim):
        time_in_rome=self.get_time_in_rome()
        rounded=self.rounded_to_the_last_5th_minute_epoch(int(time_in_rome.timestamp()))
        msg_hash=self.encode_unsigned(resource,str(rounded))
        bytes_signature=HexBytes(signature)
        print("is authenticated: "+str(self.authenticate_signature(signature,msg_hash,claim)))
        return self.authenticate_signature(signature,msg_hash,claim)
