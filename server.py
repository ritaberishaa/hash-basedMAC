import hashlib
import hmac
import logging
import os 
import socket

# Setup i logging
logging.basicConfig(filename='server.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


# marrja e shared secret key prej environment variable
shared_secret_key = os.getenv('SHARED_SECRET_KEY')
if shared_secret_key is None:
    logging.error("SHARED_SECRET_KEY environment variable not set.")
    exit(1)
shared_secret_key = shared_secret_key.encode()

def verify_hmac(received_message, received_hmac):
    calculated_hmac = hmac.new(shared_secret_key, received_message, hashlib.sha256).digest()
    return hmac.compare_digest(calculated_hmac, received_hmac)

# setup per serverin
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 12345)
server_socket.bind(server_address)
server_socket.listen(1)
#per logging
logging.info("Server started and awaiting messages...")

while True:
    client_socket, client_address = server_socket.accept()
    logging.info(f"Connection from {client_address}")
    try:
        message_length = int.from_bytes(client_socket.recv(4), 'big')
        received_message = client_socket.recv(message_length)
        received_hmac = client_socket.recv(32)

        logging.info(f"Message received with HMAC: [{received_message.decode()} | {received_hmac.hex()}]")

        if verify_hmac(received_message, received_hmac):
            response = "Message verified successfully. Integrity and authenticity confirmed."
            logging.info(response)
        else:
            response = "Message verification failed."
            logging.error(response)
        
        client_socket.send(response.encode())  # me kthy response back to client

    finally:
        client_socket.close()
