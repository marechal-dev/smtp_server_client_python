import socket as socket_package
from threading import Thread

from Email import Email
from EmailAccount import EmailAccount
from MailBox import MailBox

from MessagesDictionary import MESSAGES_DICTIONARY

HOST_ADDRESS = '127.0.0.1'
PORT = 5000
MAX_BUFFER_SIZE = 1024
DOMAIN = '@arpa.net'

CONNECTION_DETAILS = (HOST_ADDRESS, PORT)

registered_accounts: [MailBox] = []
alive_threads = []


def user_is_registered(user: MailBox, username: str):
    if user.userData.username == username:
        return True
    else:
        return False


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
            while received_command == MESSAGES_DICTIONARY.get('user_wants_to_create_new_account'):
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

            while received_command == MESSAGES_DICTIONARY.get('user_wants_to_login'):
                received_client_credentials = connection.recv(MAX_BUFFER_SIZE).decode('utf-8')
                user_credentials = received_client_credentials.split(';')

                there_are_registered_accounts = len(registered_accounts) > 0

                if there_are_registered_accounts:
                    user_account_exists = any(
                        user["userData"]["username"] == user_credentials[0] for user in registered_accounts
                    )

                    if user_account_exists:
                        connection.send(MESSAGES_DICTIONARY.get('found_account').encode('utf-8'))

                        account_data = list(
                            filter(
                                lambda user: user_is_registered(user, user_credentials[0]), registered_accounts
                            )
                        )[0]

                        if account_data.userData.password == user_credentials[1]:

                            there_are_messages_in_the_box = len(account_data.mailBox) > 0
                            if there_are_messages_in_the_box:
                                connection.send(f'{len(account_data.mailBox)}'.encode('utf-8'))

                                for email in account_data.mailBox:
                                    formatted_email_details = f'{email.sender};{email.receiver};{email.timestamp}'

                                    encoded_email_details = formatted_email_details.encode('utf-8')
                                    encoded_email_body = f'{email.content}'.encode('utf-8')
                                    connection.send(encoded_email_details)
                                    connection.send(encoded_email_body)
                            else:
                                connection.send(MESSAGES_DICTIONARY.get('empty_box').encode('utf-8'))
                        else:
                            connection.send(MESSAGES_DICTIONARY.get('password_incorrect').encode('utf-8'))
                else:
                    connection.send(MESSAGES_DICTIONARY.get('no_registered_accounts').encode('utf-8'))

                new_command = connection.recv(MAX_BUFFER_SIZE).decode('utf-8')
                received_command = new_command

            while received_command == MESSAGES_DICTIONARY.get('user_wants_to_send_email'):
                sender_address = connection.recv(MAX_BUFFER_SIZE).decode('utf-8')
                receiver_address = connection.recv(MAX_BUFFER_SIZE).decode('utf-8')

                receiver_account_exists = any(
                    user["userData"]["address"] == receiver_address for user in registered_accounts
                )

                if receiver_account_exists:
                    message_content = connection.recv(MAX_BUFFER_SIZE).decode('utf-8')

                    new_email = Email(receiver_address, sender_address, message_content)
                    print(new_email.__str__())

                    for account in registered_accounts:
                        if account.userData.address == receiver_address:
                            account.mailBox.append(new_email)
                else:
                    connection.send(MESSAGES_DICTIONARY.get('receiver_not_found').encode('utf-8'))





