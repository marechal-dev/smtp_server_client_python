import socket as socket_package

HOST_ADDRESS = '127.0.0.1'
PORT = 5000
MAX_PACKET_SIZE = 1024

CONNECTION_DETAILS = (HOST_ADDRESS, PORT)

with socket_package.socket(
    socket_package.AF_INET,
    socket_package.SOCK_STREAM
) as smtp_server:
    smtp_server.bind(CONNECTION_DETAILS)
    smtp_server.listen()
    connection, address = smtp_server.accept()
    with connection:
        print(f'Connection details: {connection}')
        print(f'Connection address: {address}')
        while True:
            received_data = connection.recv(MAX_PACKET_SIZE)
            print(f'Received from {address}: {received_data}')
            connection.sendall(received_data)


