import hashlib
import hmac
import logging
import os
import socket

# Setup i logging
logging.basicConfig(filename='client.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# gjithashtu edhe shared secret key
#fillimisht n terminal para se me bo cd to this folder, shembull: export SHARED_SECRET_KEY=qelesi123
#edhe duhet me u bo export ne te dy terminalet
shared_secret_key = os.getenv('SHARED_SECRET_KEY')
if shared_secret_key is None:
    logging.error("SHARED_SECRET_KEY environment variable not set.")
    exit(1)
shared_secret_key = shared_secret_key.encode()

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 12345)
client_socket.connect(server_address)

message = input("Enter your message: ")
hmac_signature = hmac.new(shared_secret_key, message.encode(), hashlib.sha256).digest()

client_socket.send(len(message).to_bytes(4, 'big'))
client_socket.send(message.encode())
client_socket.send(hmac_signature)

logging.info(f"Sending message with HMAC: [{message} | {hmac_signature.hex()}]")
response = client_socket.recv(1024).decode()  
logging.info("Server response: " + response)

client_socket.close()