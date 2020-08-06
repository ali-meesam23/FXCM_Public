import socket
import sys
import json

HOST, PORT = "localhost", 5000

# Create a socket (SOCK_STREAM means a TCP socket)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST,PORT))
print(f"SOCKET ESTABLISHED {sock}")
try:
    # Receive data from the server and shut down
    
    received = sock.recv(1024)

finally:
    sock.close()

print(f"Received: {received}")