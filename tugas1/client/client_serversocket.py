import os
import socket
import sys

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

# create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# get local machine name
host = socket.gethostname()

# set a port number
port = 9999

# connect to the server
client_socket.connect((host, port))

# receive data from the server
data = client_socket.recv(1024).decode()

print(f'Received data from the server: {data}')

# send a message to the server
message = input('Enter a message to send to the server: ')
client_socket.send(message.encode())

# Receive the status
status = client_socket.recv(1024).decode()

if status != 'OK':
    print(status)
    client_socket.close()
    sys.exit(1)

header = client_socket.recv(1024).decode()
print(header)

file_name = header.split('file-name: ')[1].split(',')[0]
file_size = int(header.split('file-size: ')[1].split(',')[0])
file_path = os.path.join(BASE_DIR, 'files', file_name)

print(f'File name: {file_name}')
print(f'File size: {file_size}')

with open(file_path, 'wb') as f:
    while True:
        data = client_socket.recv(1024)
        if not data:
            break
        f.write(data)

# close the connection
client_socket.close()
