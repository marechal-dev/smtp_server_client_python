from classes.MailBox import MailBox


def print_main_menu():
    print('Bem-vindo ao Cliente de E-mail ARPA.net')
    print('O que deseja fazer?')
    print('(Digite o número correspondente a opção do menu)')
    print('1) Cadastrar')
    print('2) Entrar')


def user_is_registered(user: MailBox, username: str):
    if user.userData.username == username:
        return True
    else:
        return False
