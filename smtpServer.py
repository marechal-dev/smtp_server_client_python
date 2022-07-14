import socket as socket_package
from threading import Thread

from EmailAccount import EmailAccount
from MailBox import MailBox

from MessagesDictionaries import TO_SEND_SERVER_SIDE_MESSAGES, RECEIVED_SERVER_SIDE_MESSAGES

HOST_ADDRESS = '127.0.0.1'
PORT = 5000
MAX_BUFFER_SIZE = 1024
DOMAIN = '@arpa.net'

CONNECTION_DETAILS = (HOST_ADDRESS, PORT)

registered_accounts: [MailBox] = []
alive_threads = []

with socket_package.socket(
    socket_package.AF_INET,
    socket_package.SOCK_STREAM
) as smtp_server:
    smtp_server.bind(CONNECTION_DETAILS)
    smtp_server.listen()
    while True:
        (connection, address) = smtp_server.accept()
        with connection:
            print(f'Connection details: {connection}')
            print(f'Connection address: {address}')

            received_command = connection.recv(MAX_BUFFER_SIZE).decode('utf-8')
            while received_command == RECEIVED_SERVER_SIDE_MESSAGES.get('user_wants_to_create_new_account'):
                received_data = connection.recv(MAX_BUFFER_SIZE).decode('utf-8')
                new_account_data = received_data.split(';')
                new_account = EmailAccount(
                    new_account_data[0],
                    new_account_data[1],
                    DOMAIN,
                    new_account_data[2]
                )
                new_mailbox = MailBox(new_account)
                registered_accounts.append(new_mailbox)

                print(registered_accounts[-1].__str__())
                new_command = connection.recv(MAX_BUFFER_SIZE).decode('utf-8')

                received_command = new_command
                break

            while received_command == RECEIVED_SERVER_SIDE_MESSAGES.get('user_wants_to_login'):
                received_client_credentials = connection.recv(MAX_BUFFER_SIZE).decode('utf-8')
                user_credentials = received_client_credentials.split(';')

                if len(registered_accounts) > 0:
                    for account in registered_accounts:
                        if account.userData.username == user_credentials[0]:
                            if account.userData.password == user_credentials[1]:
                                connection.send(TO_SEND_SERVER_SIDE_MESSAGES.get('found_account').encode('utf-8'))

                                if len(account.mailBox) > 0:
                                    connection.send(f'{len(account.mailBox)}'.encode('utf-8'))

                                    for email in account.mailBox:
                                        formatted_email = f'{email.sender};{email.receiver};{email.timestamp};{email.content}'
                                        encoded_email_message = formatted_email.encode('utf-8')
                                        connection.send(encoded_email_message)

                                break
                            else:
                                connection.send(TO_SEND_SERVER_SIDE_MESSAGES.get('password_incorrect').encode('utf-8'))
                                break
                    else:
                        connection.send(b'NOACC')
                else:
                    connection.send(b'NOACCS')
                break


