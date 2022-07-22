from socket import socket
import socket as socket_package

from MessagesDictionary import MESSAGES_DICTIONARY

from utils import print_main_menu

HOST_ADDRESS = '127.0.0.1'
PORT = 5000
MAX_BUFFER_SIZE = 1024
DOMAIN = '@arpa.net'

CONNECTION_DETAILS = (HOST_ADDRESS, PORT)


def print_email(email_data: list[str], email_body: str):
    print(email_data)
    print(f'Enviado por: {email_data[0]}\n')
    print(f'Remetente: {email_data[1]}\n')
    print(f'Assunto: {email_data[2]}\n')
    print(f'Enviado em: {email_data[3]}\n')
    print('Conteúdo:\n')
    print(email_body)
    return


def handle_send_email(client: socket, username: str):
    while True:
        client.send(MESSAGES_DICTIONARY.get('user_wants_to_send_email').encode('utf-8'))
        receiver_address = input('Digite o endereço do destinatário: ')

        client.send(receiver_address.encode('utf-8'))

        receiver_exists_message = client.recv(MAX_BUFFER_SIZE).decode('utf-8')
        receiver_exists = receiver_exists_message == MESSAGES_DICTIONARY.get('receiver_found')
        if receiver_exists:
            current_user_username = username
            sender_address = f'{current_user_username}{DOMAIN}'
            email_subject = input('Assunto: ')
            email_body = input('Mensagem: ')
            details_message = f'{receiver_address};{sender_address};{email_subject}'.encode('utf-8')
            body_message = email_body.encode('utf-8')

            client.send(details_message)
            client.send(body_message)
            break
        else:
            print('Remetente inexistente. Deseja tentar novamente?')
            print('1) Sim')
            print('2) Não')
            option = int(input('Opção: '))

            if option == 1:
                continue
            elif option == 2:
                break
    return


def handle_read_email(client: socket, email_box_size: int, username: str):
    while True:
        client.send(MESSAGES_DICTIONARY.get('user_wants_to_read_email').encode('utf-8'))

        print(f'Qual email deseja ler?')
        print(f'Selecione um número de 1 a {email_box_size}')

        # O input do email selecionado é diminuido de 1 para selecionar um email
        # em uma lista no lado do servidor
        selected_email_index = str(int(input('Opção: ')) - 1)

        # Enviamos o índice do email desejado e o nome de usuário do remetente
        client.send(selected_email_index.encode('utf-8'))
        client.send(username.encode('utf-8'))

        # Esperamos os dados do email e o corpo da mensagem
        email_data = client.recv(MAX_BUFFER_SIZE).decode('utf-8').split(';')
        email_body = client.recv(MAX_BUFFER_SIZE).decode('utf-8')

        print_email(email_data, email_body)

        print('Deseja ler algum outro email?')
        print('1) Sim')
        print('2) Não')
        read_loop_option = int(input('Opção: '))

        if read_loop_option == 1:
            client.send(MESSAGES_DICTIONARY.get('user_wants_to_read_email').encode('utf-8'))
            continue
        else:
            break


def handle_main_menu(client: socket, username: str):
    # Aguardamos receber o tamanho da caixa de entrada
    email_box_size = int(client.recv(MAX_BUFFER_SIZE).decode('utf-8'))

    print(f'Bem-vindo {username}! Você tem {email_box_size} emails na caixa de entrada.')

    print('O que deseja fazer agora?')
    print('1) Enviar E-mail')

    if email_box_size > 0:
        print('2) Ler E-mails')
        print('3) Sair')
    else:
        print('2) Sair')

    # Esperamos o novo comando
    new_option = int(input('Opção: '))

    if new_option == 1:
        handle_send_email(client, username)
    elif new_option == 2 and email_box_size > 0:
        handle_read_email(client, email_box_size, username)
    elif new_option == 2 and new_option == 0:
        client.close()


def handle_login(client: socket):
    # Pedimos as credenciais
    username = input('Digite seu nome de usuário: ')
    password = input('Digite sua senha: ')

    # Formatamos de forma conveniente para o servidor
    formatted_credentials = f'{username};{password}'.encode('utf-8')

    # E enviamos as credenciais!
    client.send(formatted_credentials)

    # Aguardamos uma resposta para saber se a conta existe
    received_message = client.recv(MAX_BUFFER_SIZE).decode('utf-8')
    account_was_found = received_message == MESSAGES_DICTIONARY.get('found_account')

    # Caso sim...
    if account_was_found:
        print('Conta encontrada!')

        # Aguardamos outra resposta para saber se a senha está correta
        received_message = client.recv(MAX_BUFFER_SIZE).decode('utf-8')
        print(received_message)
        password_is_correct = received_message == MESSAGES_DICTIONARY.get('correct_password')

        # Caso esteja...
        if password_is_correct:
            print('Senha correta!')

            handle_main_menu(client, username)
        else:
            print('Senha incorreta!')
    elif received_message == MESSAGES_DICTIONARY.get('incorrect_credentials'):
        print('Conta inexistente')


def handle_create_account(client: socket):
    # Avise o servidor que queremos criar uma nova conta
    client.send(MESSAGES_DICTIONARY.get('user_wants_to_create_new_account').encode('utf-8'))

    # Inserimos os dados
    name = input('Nome: ')
    username = input('Nome de usuário: ')
    password = input('Senha: ')

    # Formatamos a mensagem de forma conveniente para o servidor
    formatted_content = f'{name};{username};{password}'
    # Fazemos encoding
    encoded_message = formatted_content.encode('utf-8')

    # E mandamos!
    client.send(encoded_message)


with socket_package.socket(
    socket_package.AF_INET,
    socket_package.SOCK_STREAM
) as smtp_client:
    # Conectamos no servidor
    smtp_client.connect(CONNECTION_DETAILS)
    print_main_menu()

    # Uma opção deve ser selecionada...
    selected_option = int(input('Opção: '))

    # Caso seja para criar uma conta
    if selected_option == 1:
        handle_create_account(smtp_client)

        # Perguntamos ao senhor Client se ele quer logar ou sair
        print('Deseja fazer mais alguma coisa?')
        print('1) Entrar')
        print('2) Sair')

        next_step = int(input('Opção: '))

        # Caso ele queira entrar...
        if next_step == 1:
            smtp_client.send(MESSAGES_DICTIONARY.get('user_wants_to_login').encode('utf-8'))
            handle_login(smtp_client)
        elif next_step == 2:
            smtp_client.close()
    elif selected_option == 2:
        smtp_client.send(MESSAGES_DICTIONARY.get('user_wants_to_login').encode('utf-8'))
        handle_login(smtp_client)
