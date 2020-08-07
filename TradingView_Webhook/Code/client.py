import socket

HEADER = 1024 # Defining a header for message protocol wih 124 bytes
PORT = 5050

FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECTED"
SERVER = '192.168.0.24'
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Now connect to the server
client.connect(ADDR)


def send(msg):
    message =  msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    # padding the message to HEADER bytes
    send_length += b" " * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)

#
# send("Hello World!")
# input()
# send("Hello Mars!")
# input()
# send("Hello Tim!")
# input()
# send(DISCONNECT_MESSAGE)