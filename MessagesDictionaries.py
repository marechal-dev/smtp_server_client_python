TO_SEND_MESSAGES = {
    'FOR_SERVER_SIDE': {
        'found_account': 'ACC',
        'password_incorrect': 'INCORRECTPASS',
        'account_not_found': 'NOACC',
        'no_registered_accounts': 'NOACCS'
    },
    'FOR_CLIENT_SIDE': {}
}

RECEIVED_MESSAGES = {
    'FOR_SERVER_SIDE': {
        'user_wants_to_create_new_account': '1',
        'user_wants_to_login': '2'
    },
    'FOR_CLIENT_SIDE': {
        'found_account': 'ACC',
        'account_not_found': 'NOACC',
        'incorrect_password': 'INCORRECTPASS',
        'no_registered_accounts': 'NOACCS'
    }
}

TO_SEND_SERVER_SIDE_MESSAGES = TO_SEND_MESSAGES.get('FOR_SERVER_SIDE')
RECEIVED_SERVER_SIDE_MESSAGES = RECEIVED_MESSAGES.get('FOR_SERVER_SIDE')

TO_SEND_CLIENT_SIDE_MESSAGES = TO_SEND_MESSAGES.get('FOR_CLIENT_SIDE')
RECEIVED_CLIENT_SIDE_MESSAGES = RECEIVED_MESSAGES.get('FOR_CLIENT_SIDE')

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
