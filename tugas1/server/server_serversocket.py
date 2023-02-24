import os
import socket
import sys

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

# create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# get local machine name
host = socket.gethostname()

# set a port number
port = 9999

# bind the socket to a public host and port
server_socket.bind((host, port))

# listen for incoming connections
server_socket.listen(1)

print('Waiting for a client to connect...')

try:
    while True:
        # establish a connection
        client_socket, client_address = server_socket.accept()

        print(f'Connection established with {client_address}')

        # send a welcome message to the client
        client_socket.send('Welcome to the server!'.encode())

        # receive data from the client
        data = client_socket.recv(1024).decode()

        command, filename = data.split(maxsplit=1)

        if command != 'download':
            print(f'Unknown command: {command}')
            client_socket.send('Unknown command'.encode())
            continue

        print(f'Requested file: {filename}')
        client_socket.send('OK'.encode())

        filepath = os.path.join(BASE_DIR, 'files', filename)
        filesize = os.path.getsize(filepath)

        header = f'\tfile-name: {filename},\r\n\tfile-size: {filesize},\r\n\n\n'.encode()

        client_socket.send(header)

        with open(filepath, 'rb') as f:
            while True:
                data = f.read(1024)
                if not data:
                    break
                client_socket.send(data)

        # close the connection
        client_socket.close()

except KeyboardInterrupt:
    server_socket.close()
    sys.exit(0)
