MESSAGES_DICTIONARY = {
    'found_account': 'ACC',
    'account_not_found': 'NOACC',
    'incorrect_password': 'INCORRECTPASS',
    'no_registered_accounts': 'NOACCS',
    'empty_box': 'EMPTYBOX',
    'receiver_not_found': 'NORCV',
    'user_wants_to_create_new_account': '1',
    'user_wants_to_login': '2',
    'user_wants_to_send_email': '3'
}

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
