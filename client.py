import hashlib
import hmac
import logging
import os
import socket

# konfigurohet sistemit i regjistrimit te logjeve per te ruajtur logjet ne nje file specifik 
logging.basicConfig(filename='client.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# kontrollohet dhe merret celesi i perbashket nga environment variable, nese ky celes nuk vendoset programi ndalon ekzekutimin dhe jep nje mesazh gabimi
shared_secret_key = os.getenv('SHARED_SECRET_KEY')
if shared_secret_key is None:
    logging.error("SHARED_SECRET_KEY environment variable not set.")
    print("Key environment variable not set.")
    exit(1)
shared_secret_key = shared_secret_key.encode()

# krijohet nje socket klienti dhe lidhet me serverin ne adresen edhe portin e specifikuar
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 12345)
client_socket.connect(server_address)

# perdoruesi jep mesazhin, klienti gjeneron nje HMAC per ate mesazh duke perdor celesin dhe funksionin hash SHA-256
message = input("Enter your message: ")
hmac_signature = hmac.new(shared_secret_key, message.encode(), hashlib.sha256).digest()

# mesazhi dhe HMAC dergohen te serveri ne formatin e specifikuar
client_socket.send(len(message).to_bytes(4, 'big'))
client_socket.send(message.encode())
client_socket.send(hmac_signature)

# klienti pret pergjigjen nga serveri, e dekodon ate dhe e regjistron ne log dhe poashtu shfaqet ne ekran
logging.info(f"Sending message with HMAC: [{message} | {hmac_signature.hex()}]")
print(f"Sending message with HMAC: [{message} | {hmac_signature.hex()}]")
response = client_socket.recv(1024).decode()  
logging.info("Server response: " + response)
print("Server response:", response)

# ne fund, socketi i klientit mbyllet per te liru burimet
client_socket.close()