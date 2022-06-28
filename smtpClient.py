import socket as socket_package

HOST_ADDRESS = '127.0.0.1'
PORT = 5000
MAX_PACKET_SIZE = 1024

CONNECTION_DETAILS = (HOST_ADDRESS, PORT)

with socket_package.socket(
    socket_package.AF_INET,
    socket_package.SOCK_STREAM
) as smtp_client:
    smtp_client.connect(CONNECTION_DETAILS)
    smtp_client.sendall(b'Hello motherfuckers')
    received_data = smtp_client.recv(MAX_PACKET_SIZE)

print(f'Received {received_data!r}')
