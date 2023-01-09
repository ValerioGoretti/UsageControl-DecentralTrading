# echo-client.py

import socket

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 5555  # The port used by the server
name="facebook"

private_key="MIIBOQIBAAJBAMhZt1v5EHcjgWMlaXM4ImwMdL9Tpr907ZKkhz46EdWzwIUkW4BD3njLc094QvyN39vSAOoOi597B8GKR7mX+esCAwEAAQJAJvisngtYlJQneu2wEWV97J6PpxfSe7N28utmE0igZ3zzUEcQ0BV38LdB3UB5xg0TYeF8ARr7vyq/yFhhQeDvAQIhAPF6tpGo7rtE6vbZfuYNOneAJF6YtSDyh5wgk1+PbIIhAiEA1GXfbaTC8W/RAv9I/GmGd2ZssUlq1JU0WF5e5bWnEosCIB7s0T68PL6c595vIjJCFW/CaGX49pFengFfpqABVSshAiBZ70DqBkfdP4F7CWl4J56eVCpV70Zi+UKO4HbCQWaa/QIgfYn07H9z+9V2R76Gl+2L4EVdk+NK0Y+TJWm0TSFd1f4="
public_key="MFwwDQYJKoZIhvcNAQEBBQADSwAwSAJBAMhZt1v5EHcjgWMlaXM4ImwMdL9Tpr907ZKkhz46EdWzwIUkW4BD3njLc094QvyN39vSAOoOi597B8GKR7mX+esCAwEAAQ=="

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

print("====Facebook====")

i=''
while(i!=':exit'):
    print("INSERISCI UNA PAROLA ->")
    data = s.recv(1024)
    i=input()
    #i=i+"|"+name
    i_bites=bytes(i, 'ascii')
    s.send(i_bites)
    print (data.decode())


print("DISCONNESSO")
#print(f"Received {data!r}")
