import socket
import threading

HEADER = 1024 # Defining a header for message protocol wih 124 bytes
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
# Bind it to an address
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECTED"

# Making the socket to open it to other connections
server = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
# Binding 'server' socket to address ADDR
server.bind(ADDR)



# Set it up for listening and let it wait for the connections

def handle_client(conn, addr):
    """
    Handle all of the comms between client and server
    """
    print(f"[NEW CONNECTION] {addr} connected.")

    connected = True

    while connected:
        # Getting message from the server and need to define a protocol of sending and receiving messages
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            # Actual Message
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                connected = False
            print(f"[{addr}] {msg}")

    conn.close()

def start():
    # start listening to those connections and pass to handle connections
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        # Will wait for a new connection on the server
        conn, addr = server.accept()   
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() -1}")


print("[STARTING] Server is starting...")
start()
