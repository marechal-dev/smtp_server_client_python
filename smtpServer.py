import socket as socket_package
import sqlite3
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

            # Recebemos um comando para realizar uma operação
            received_command = connection.recv(MAX_BUFFER_SIZE).decode('utf-8')

            # Caso o comando seja de criar conta
            while received_command == MESSAGES_DICTIONARY.get('user_wants_to_create_new_account'):
                # Recebemos os dados
                received_data = connection.recv(MAX_BUFFER_SIZE).decode('utf-8').split(';')

                # Criamos uma nova conta
                new_account = EmailAccount(
                    received_data[0],
                    received_data[1],
                    DOMAIN,
                    received_data[2]
                )

                # Criamos uma nova caixa de emails
                new_mailbox = MailBox(new_account)

                # Inserimos a mesma no array de contas registradas
                registered_accounts.append(new_mailbox)

                print(registered_accounts[-1].__str__())

                # Esperamos um novo comando
                new_command = connection.recv(MAX_BUFFER_SIZE).decode('utf-8')
                received_command = new_command

                break

            # Caso o comando seja de realizar login
            while received_command == MESSAGES_DICTIONARY.get('user_wants_to_login'):
                # Recebemos as credenciais
                received_client_credentials = connection.recv(MAX_BUFFER_SIZE).decode('utf-8')

                # Formatamos as credenciais
                user_credentials = received_client_credentials.split(';')

                # Existem contas registradas?
                there_are_registered_accounts = len(registered_accounts) > 0

                # Caso sim...
                if there_are_registered_accounts:
                    # Verificamos se a conta desejada existe
                    user_account_exists = any(
                        user["userData"]["username"] == user_credentials[0] for user in registered_accounts
                    )

                    # Caso exista...
                    if user_account_exists:
                        # Enviamos uma mensagem indicando que a conta foi achada
                        connection.send(MESSAGES_DICTIONARY.get('found_account').encode('utf-8'))

                        # Filtamos os dados
                        account_data = list(
                            filter(
                                lambda user: user_is_registered(user, user_credentials[0]), registered_accounts
                            )
                        )[0]

                        # Verificamos se a senha recebida bate com a salva em memória
                        if account_data.userData.password == user_credentials[1]:

                            # Existem emails nessa conta?
                            there_are_messages_in_the_box = len(account_data.mailBox) > 0

                            # Caso sim...
                            if there_are_messages_in_the_box:
                                # Enviamos a quantidade de emails
                                connection.send(f'{len(account_data.mailBox)}'.encode('utf-8'))


                                # E para cada email
                                for email in account_data.mailBox:
                                    # Formatamos os detalhes (remetente, destinatário e hora de envio)
                                    formatted_email_details = f'{email.sender};{email.receiver};{email.timestamp}'

                                    # Fazemos encoding dos detalhes
                                    encoded_email_details = formatted_email_details.encode('utf-8')

                                    # E do corpo do email
                                    encoded_email_body = f'{email.content}'.encode('utf-8')

                                    # Enviamos ambos e pronto!
                                    connection.send(encoded_email_details)
                                    connection.send(encoded_email_body)
                            else:
                                # Caso não existam emails, enviamos uma mensagem indicando isso
                                connection.send(MESSAGES_DICTIONARY.get('empty_box').encode('utf-8'))
                        else:
                            # Caso não bata, enviamos uma mensagem indicando isso
                            connection.send(MESSAGES_DICTIONARY.get('password_incorrect').encode('utf-8'))
                else:
                    # Caso não existam, enviamos uma mensagem indicando isso
                    connection.send(MESSAGES_DICTIONARY.get('no_registered_accounts').encode('utf-8'))

                # Esperamos o próximo comando
                new_command = connection.recv(MAX_BUFFER_SIZE).decode('utf-8')
                received_command = new_command

                break

            # Caso o comando seja de enviar um email
            while received_command == MESSAGES_DICTIONARY.get('user_wants_to_send_email'):
                # Primeiro, recebemos o endereço do remetente e do destinatário
                sender_address = connection.recv(MAX_BUFFER_SIZE).decode('utf-8')
                receiver_address = connection.recv(MAX_BUFFER_SIZE).decode('utf-8')

                # Depois verificamos se o destinatário existe
                receiver_account_exists = any(
                    user["userData"]["address"] == receiver_address for user in registered_accounts
                )

                # Caso ele exista...
                if receiver_account_exists:
                    # Recebemos o conteúdo do email
                    message_content = connection.recv(MAX_BUFFER_SIZE).decode('utf-8')

                    # Criamos um novo email
                    new_email = Email(receiver_address, sender_address, message_content)
                    print('Dados do email enviado:\n')
                    print(new_email.__str__())

                    # Inserimos o email na caixa do destinatário
                    for account in registered_accounts:
                        if account.userData.address == receiver_address:
                            account.mailBox.append(new_email)
                else:
                    # Caso não exista, enviamos uma mensagem de que o destinatário não existe
                    connection.send(MESSAGES_DICTIONARY.get('receiver_not_found').encode('utf-8'))

                # Esperamos o novo comando
                new_command = connection.recv(MAX_BUFFER_SIZE).decode('utf-8')
                received_command = new_command

                break

