import socket as socket_package
from time import sleep

from classes.Email import Email
from classes.EmailAccount import EmailAccount
from classes.MailBox import MailBox


from MessagesDictionary import MESSAGES_DICTIONARY

HOST_ADDRESS = '127.0.0.1'
PORT = 5000
MAX_BUFFER_SIZE = 1024
DOMAIN = '@arpa.net'

CONNECTION_DETAILS = (HOST_ADDRESS, PORT)

registered_accounts: [MailBox] = []


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
                print(f'Handling command {received_command}...')

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

                print(registered_accounts[-1].userData.__str__())

                # Esperamos um novo comando
                new_command = connection.recv(MAX_BUFFER_SIZE).decode('utf-8')
                received_command = new_command

                break

            # Caso o comando seja de realizar login
            while received_command == MESSAGES_DICTIONARY.get('user_wants_to_login'):
                print(f'Handling command {received_command}...')

                # Recebemos as credenciais
                received_client_credentials = connection.recv(MAX_BUFFER_SIZE).decode('utf-8')

                # Formatamos as credenciais
                user_credentials = received_client_credentials.split(';')
                print(user_credentials)

                # Existem contas registradas?
                there_are_registered_accounts = len(registered_accounts) > 0

                # Caso sim...
                if there_are_registered_accounts:
                    # Verificamos se a conta desejada existe
                    user_account_exists = False

                    for user in registered_accounts:
                        if user.userData.username == user_credentials[0]:
                            user_account_exists = True
                            break

                    print(f'Usuário existe?: {user_account_exists}')

                    # Caso exista...
                    if user_account_exists:
                        # Enviamos uma mensagem indicando que a conta foi achada
                        connection.send(MESSAGES_DICTIONARY.get('found_account').encode('utf-8'))

                        # Filtramos os dados
                        account_data: MailBox

                        for account in registered_accounts:
                            if account.userData.username == user_credentials[0]:
                                account_data = account
                                break

                        print(f'Dados da conta: {account_data.userData.__str__()}')

                        # Verificamos se a senha recebida bate com a salva em memória
                        if account_data.userData.password == user_credentials[1]:
                            # Informamos o cliente que a senha está correta
                            connection.send(MESSAGES_DICTIONARY.get('correct_password').encode('utf-8'))

                            # Por algum motivo de obscuro,
                            # O send da linha cima estava concatenando seu conteúdo com o tamanho
                            # do vetor de emails do usuário.
                            # Decidi então colocar um sleep de meio segundo para parar isso
                            # """Solução temporária permanente""" aka Gambiarra
                            sleep(0.5)
                            print('ok')

                            # Existem mensagens na caixa de entrada dessa conta?
                            there_are_messages_in_the_box = len(account_data.mailBox) > 0

                            # Caso sim...
                            if there_are_messages_in_the_box:
                                # Enviamos a quantidade de mensagens para exibir no cliente
                                connection.send(f'{len(account_data.mailBox)}'.encode('utf-8'))
                            else:
                                # Caso não existam emails, enviamos uma mensagem com zero
                                connection.send('0'.encode('utf-8'))
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
                print(f'Handling command {received_command}...')

                # Primeiro, recebemos o endereço do destinatário
                receiver_address = connection.recv(MAX_BUFFER_SIZE).decode('utf-8')
                print(receiver_address)

                # Depois verificamos se o destinatário existe
                receiver_account_exists = any(
                    user.userData.address == receiver_address for user in registered_accounts
                )

                print(f'Does receiver exists? {receiver_account_exists}')

                # Caso ele exista...
                if receiver_account_exists:
                    connection.send(MESSAGES_DICTIONARY.get('receiver_found').encode('utf-8'))

                    # Recebemos os detalhes da mensagem
                    details = connection.recv(MAX_BUFFER_SIZE).decode('utf-8').split(';')
                    # Recebemos o conteúdo do email
                    message_content = connection.recv(MAX_BUFFER_SIZE).decode('utf-8')

                    # Criamos um novo email
                    new_email = Email(details[0], details[1], details[2], message_content)
                    print(f'Dados do email enviado: {new_email.__str__()}\n')

                    # Inserimos o email na caixa do destinatário
                    for account in registered_accounts:
                        if account.userData.address == receiver_address:
                            account.mailBox.append(new_email)
                            break
                else:
                    # Caso não exista, enviamos uma mensagem de que o destinatário não existe
                    connection.send(MESSAGES_DICTIONARY.get('receiver_not_found').encode('utf-8'))

                # Esperamos o novo comando
                new_command = connection.recv(MAX_BUFFER_SIZE).decode('utf-8')
                received_command = new_command

                break

            # Caso o comando seja de ler um email
            while received_command == MESSAGES_DICTIONARY.get('user_wants_to_read_email'):
                print(f'Handling command {received_command}...')

                email_index = int(connection.recv(MAX_BUFFER_SIZE).decode('utf-8'))
                sender_username = connection.recv(MAX_BUFFER_SIZE).decode('utf-8')
                account_data: MailBox

                for email in registered_accounts:
                    if email.userData.username == sender_username:
                        account_data = email
                        break

                email_data = account_data.mailBox[email_index]
                # Formatamos os detalhes (remetente, destinatário, assunto e data de envio)
                formatted_email_details = f'{email_data.sender};{email_data.receiver};{email_data.subject};{email_data.timestamp}'

                # Fazemos encoding dos detalhes
                encoded_email_details = formatted_email_details.encode('utf-8')

                # E do corpo do email
                encoded_email_body = f'{email_data.content}'.encode('utf-8')

                # Enviamos ambos e pronto!
                connection.send(encoded_email_details)
                connection.send(encoded_email_body)

                new_command = connection.recv(MAX_BUFFER_SIZE).decode('utf-8')
                received_command = new_command

                break



