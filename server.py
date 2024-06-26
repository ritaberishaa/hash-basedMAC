import hashlib
import hmac
import logging
import os 
import socket

# konfigurohet sistemit i regjistrimit te logjeve per te ruajtur logjet ne nje file specifik 
logging.basicConfig(filename='server.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# kontrollohet dhe merret celesi i perbashket nga environment variable, nese ky celes nuk vendoset programi ndalon ekzekutimin dhe jep nje mesazh gabimi
shared_secret_key = os.getenv('SHARED_SECRET_KEY')
if shared_secret_key is None:
    logging.error("SHARED_SECRET_KEY environment variable not set.")
    print("Key environment variable not set.")
    exit(1)
shared_secret_key = shared_secret_key.encode()

# funksioni qe gjeneron nje HMAC per mesazhin e pranuar dhe e krahason ate me HMAC e pranuar per te verifiku integritetin dhe autenticitetin e mesazhit
def verify_hmac(received_message, received_hmac):
    calculated_hmac = hmac.new(shared_secret_key, received_message, hashlib.sha256).digest()
    return hmac.compare_digest(calculated_hmac, received_hmac)

# krijohet nje socket server dhe lidhet ne adresen dhe portin e specifikum
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 12345)
server_socket.bind(server_address)
server_socket.listen(1)
# per logging edhe printim
logging.info("Server started and awaiting messages...")
print("Server started and awaiting messages...")

while True:
    # pranon lidhjet e klienteve dhe regjistron adresen e klientit
    client_socket, client_address = server_socket.accept()
    logging.info(f"Connection from {client_address}")
    try:
        # merr mesazhin
        message_length = int.from_bytes(client_socket.recv(4), 'big')
        received_message = client_socket.recv(message_length)
        received_hmac = client_socket.recv(32)
        
        # printon mesazhin e marre 
        logging.info(f"Message received with HMAC: [{received_message.decode()} | {received_hmac.hex()}]")
        print(f"Message received with HMAC: [{received_message.decode()} | {received_hmac.hex()}]")
        print("Validating HMAC...")

        # verifikon HMAC
        if verify_hmac(received_message, received_hmac):
            response = "Message verified successfully. Integrity and authenticity confirmed."
            logging.info(response)
            print(response)
        else:
            response = "Message verification failed."
            logging.error(response)
            print(response)

        client_socket.send(response.encode())  # me kthy response back to client

    # mbyll lidhjet me klientin
    finally:
        client_socket.close()
