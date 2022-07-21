import socket as socket_package

from MessagesDictionary import MESSAGES_DICTIONARY

from utils import print_main_menu, print_mail_box_menu

HOST_ADDRESS = '127.0.0.1'
PORT = 5000
MAX_BUFFER_SIZE = 1024
DOMAIN = '@arpa.net'

CONNECTION_DETAILS = (HOST_ADDRESS, PORT)

with socket_package.socket(
    socket_package.AF_INET,
    socket_package.SOCK_STREAM
) as smtp_client:
    smtp_client.connect(CONNECTION_DETAILS)
    print_main_menu()

    selected_option = int(input('Opção: '))
    if selected_option == 1:
        name = input('Nome: ')
        username = input('Nome de usuário: ')
        password = input('Senha: ')
        formatted_content = f'{name};{username};{password}'
        encoded_message = formatted_content.encode('utf-8')
        smtp_client.send(MESSAGES_DICTIONARY.get('user_wants_to_register'))
        smtp_client.send(encoded_message)

        print('Deseja fazer mais alguma coisa?')
        print('1) Entrar')
        print('2) Sair')
        next_step = int(input('Opção: '))

        if next_step == 1:
            formatted_credentials = f'{username};{password}'
            encoded_credentials_message = formatted_credentials.encode('utf-8')

            smtp_client.send(MESSAGES_DICTIONARY.get('user_wants_to_login'))
            smtp_client.send(encoded_credentials_message)
            received_message = smtp_client.recv(MAX_BUFFER_SIZE).decode('utf-8')

            if received_message == MESSAGES_DICTIONARY.get('found_account'):
                print_mail_box_menu(user_name)
                mailbox_size = int(smtp_client.recv(MAX_BUFFER_SIZE).decode('utf-8'))

                for i in range(0, mailbox_size - 1):
                    email_details = smtp_client.recv(MAX_BUFFER_SIZE).decode('utf-8')
                    email_body = smtp_client.recv(MAX_BUFFER_SIZE).decode('utf-8')


            elif received_message == MESSAGES_DICTIONARY.get('incorrect_credentials'):
                print('Conta inexistente')
        elif next_step == 2:
            smtp_client.close()
    elif selected_option == 2:
        smtp_client.send(MESSAGES_DICTIONARY.get('user_wants_to_login'))
