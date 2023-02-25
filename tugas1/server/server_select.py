import os
import select
import socket
import sys
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../..')))

from utils.bcolors import bcolors

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

# create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# get local machine name
host = socket.gethostname()

# set a port number
port = 9999

server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((host, port))
server_socket.listen(5)

# Set up a list of sockets to monitor
sockets_list = [server_socket]

# Set up a dictionary to keep track of clients and their data
clients = {}

print('\n' + bcolors.OKGREEN + "Server started." + bcolors.ENDC + '\n')

while True:
    # Monitor the sockets for incoming data
    read_sockets, _, _ = select.select(sockets_list, [], [])

    for sock in read_sockets:
        # Handle incoming connections
        if sock == server_socket:
            client_socket, client_address = server_socket.accept()
            sockets_list.append(client_socket)
            clients[client_socket] = {'data': b''}
            print(bcolors.OKBLUE +
                  f"New connection from {client_address[0]}:{client_address[1]}" + bcolors.ENDC)

        # Handle incoming data from clients
        else:
            try:
                data = sock.recv(1024)
                if data:
                    clients[sock]['data'] += data
                else:
                    # No more data from the client, remove the socket
                    print(
                        bcolors.FAIL + f"Connection closed by {sock.getpeername()[0]}" + bcolors.ENDC)
                    sockets_list.remove(sock)
                    del clients[sock]
            except:
                # Connection closed unexpectedly, remove the socket
                print(
                    bcolors.FAIL + f"Connection closed by {sock.getpeername()[0]}" + bcolors.ENDC)
                sockets_list.remove(sock)
                del clients[sock]

    # Send data back to all connected clients
    for sock in clients:
        if clients[sock]['data']:
            if clients[sock]['data'] == b'exit':
                response = bcolors.FAIL+'Goodbye!'+bcolors.ENDC
                sock.sendall(response.encode())
                continue

            response = bcolors.OKBLUE + f"You sent: {clients[sock]['data'].decode()}" + bcolors.ENDC
            sock.sendall(response.encode())
            clients[sock]['data'] = b''
