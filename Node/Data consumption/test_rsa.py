import rsa
import base64

# Generate private and public keys
(pubkey, privkey) = rsa.newkeys(512)

# Generate a random message
message = 'Hello World'

# Encrypt the message with the public key
encrypted_message = rsa.encrypt(message.encode('ascii'), pubkey)

# Decrypt the message with the private key
decrypted_message = rsa.decrypt(encrypted_message, privkey)

# Print the message
public_key=pubkey.save_pkcs1(format='PEM')
print(public_key)
