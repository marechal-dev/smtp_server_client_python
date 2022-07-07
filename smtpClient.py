import socket as socket_package

HOST_ADDRESS = '127.0.0.1'
PORT = 5000
MAX_PACKET_SIZE = 1024
DOMAIN = '@arpa.net'

CONNECTION_DETAILS = (HOST_ADDRESS, PORT)


def print_main_menu():
    print('Bem-vindo ao Cliente de E-mail ARPA.net')
    print('O que deseja fazer?')
    print('(Digite o número correspondente a opção do menu)')
    print('1) Cadastrar')
    print('2) Entrar')


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
        smtp_client.send(b'1')
        smtp_client.send(encoded_message)

        print('Deseja fazer mais alguma coisa?')
        print('1) Entrar')
        print('2) Sair')
        next_step = int(input('Opção: '))

        if next_step == 1:
            smtp_client.send(b'2')
            smtp_client.close()
        elif next_step == 2:
            smtp_client.close()
    elif selected_option == 2:
        smtp_client.send(b'2')
        smtp_client.close()
