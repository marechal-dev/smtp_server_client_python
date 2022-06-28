import socket as socket_package
from threading import Thread

from EmailAccount import EmailAccount
from MailBox import BoxAccount

HOST_ADDRESS = '127.0.0.1'
PORT = 5000
MAX_PACKET_SIZE = 1024
DOMAIN = '@arpa.net'

CONNECTION_DETAILS = (HOST_ADDRESS, PORT)

CREATE_ACCOUNT_COMMAND = b'1'
LOGIN_COMMAND = b'2'

registered_accounts: [BoxAccount] = []
alive_threads = []

# def create_new_thread(connection, address):
#     new_thread = Thread(target=handle_connection, args=(connection, address))
#
#     if len(alive_threads) > 0:
#         alive_threads.append(new_thread.ident)
#
#     new_thread.start()

# def handle_connection():
#     print(f'Connection details: {connection}')
#     print(f'Connection address: {address}')
#
#     CLIENT_WANT_TO_CLOSE = b'0'
#     while True:
#         received_data = connection.recv(MAX_PACKET_SIZE)
#         if received_data == CREATE_ACCOUNT_COMMAND:
#             print('Criar conta')
#             break
#         elif received_data == LOGIN_COMMAND:
#             print('Logar')
#             break

with socket_package.socket(
    socket_package.AF_INET,
    socket_package.SOCK_STREAM
) as smtp_server:
    smtp_server.bind(CONNECTION_DETAILS)
    smtp_server.listen()
    while True:
        connection, address = smtp_server.accept()
        with connection:
            print(f'Connection details: {connection}')
            print(f'Connection address: {address}')

            received_data = connection.recv(MAX_PACKET_SIZE)
            while received_data:
                print(received_data.decode('utf-8'))


