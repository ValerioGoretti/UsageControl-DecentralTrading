# echo-client.py
import zmq


name="zooresearch"

private_key="MIIBOgIBAAJBAJ0XmjA7l5NERUWbpqECPK0iM7kxWhdDbiicrrrlUa8cmdfFJw6HZbjUlOulSoLZVIpHu+XyVDM6jrSDWYHYPncCAwEAAQJAX628b5wcGcn/FwJSXsZqBllKf4Ubhge/1GR518NMGQaxZRkq7A/U7EFP0Y2iBZw5iRD6zkzhrT4+huSBGTHDgQIhANmI8+6XECRSMPX7lrk1JO5dRevgtmedsJWELUHV0lFnAiEAuN6dz2FpWEIK2gAOPJ/85wblG1G11N3H4K6cYlbpMHECIHWAjIKsBoQYAWpdY6TXGAPJTiODVgPSIbghlXCiVuCxAiEAlsEbCZkTMeCxPrLa6T9CGhd6TzvjvpGYxDU/28Wp5VECIH9WyX/j2DTPZ92utx+uDEGGawtYg58DSGN/tofCbZ0r"
public_key="MFwwDQYJKoZIhvcNAQEBBQADSwAwSAJBAJ0XmjA7l5NERUWbpqECPK0iM7kxWhdDbiicrrrlUa8cmdfFJw6HZbjUlOulSoLZVIpHu+XyVDM6jrSDWYHYPncCAwEAAQ=="


# Create a ZeroMQ context
context = zmq.Context()
# Create a socket and connect to the server
host = "127.0.0.1"
port = 5555
socket = context.socket(zmq.REQ)
socket.connect("tcp://{}:{}".format(host, port))
# Send a message to the server
socket.send_string(public_key)
# Receive a response from the server
response = socket.recv()
print(response)