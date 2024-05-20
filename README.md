# Implementation of Hash-based Message Authentication Code (HMAC) on a Client-Server Model

**Overview**

This project implements a secure communication system using a Hash-based Message Authentication Code (HMAC) to verify the integrity and authenticity of messages on a Client-Server Model. The system involves both client and server components written in Python.

**Objectives**

* Apply HMAC for securing messages against tampering and forgery.
* Ensure data integrity and authenticity in client-server communications.
* Gain hands-on experience using cryptographic libraries.

**Technical Stack**

* Server: Authenticates received messages and optionally provides responses.
* Client: Sends messages with HMAC authentication codes.
* Dependencies: Uses hashlib and hmac libraries.

**Requirements**

**Shared Secret Key**
A pre-shared secret key is established and used by both the client and server. The key is retrieved from an environment variable to enhance security.

**Client-Side Message Preparation**
The client accepts user input for the message to be sent, generates an HMAC for the message using the shared secret key and SHA-256 hash function.

**Server-Side Message Verification**
The server verifies the HMAC received from the client using the shared secret key and provides confirmation of message authenticity and integrity.

**Communication Protocol**
A simple communication protocol is designed where the client sends the length of the message, the message itself, and the HMAC to the server. The server processes these components.

**User Interface**
User-friendly console interfaces are implemented for both the client and server, guiding the user through sending, receiving, and verifying messages.

**Security Practices**
The shared secret key is securely handled within both applications. Measures such as using hmac.compare_digest are implemented to prevent timing attacks.

**Logging**
Logging is included for significant actions in both the client and server, such as message transmission, HMAC generation, and verification results.

<h2>How to run</h2>

**Running the Server**
* Set the shared secret key environment variable:
  * export SHARED_SECRET_KEY="your_shared_secret_key"
* Run the server script:
  * python server.py

**Running the Client**
* Set the shared secret key environment variable:
  * export SHARED_SECRET_KEY="your_shared_secret_key"
* Run the client script:
  * python client.py
* Enter the message you want to send when prompted.

<h3>Example Console Output</h3>

**Server**



**Client**


