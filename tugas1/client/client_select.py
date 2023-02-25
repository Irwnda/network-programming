import os
import socket


BASE_DIR = os.path.dirname(os.path.realpath(__file__))

# create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# get local machine name
host = socket.gethostname()

# set a port number
port = 9999

# connect to the server
client_socket.connect((host, port))

while True:
    # send a message to the server
    message = input('Enter a message to send to the server: ')
    client_socket.send(message.encode())

    # receive data from the server
    data = client_socket.recv(1024).decode()

    print(f'Received data from the server: {data}')

    if 'Goodbye!' in data:
        client_socket.close()
        break
