from datetime import date

class Email:
    def __init__(self, receiver_address: str, sender_address: str, content: str):
        self.receiver = receiver_address
        self.sender = sender_address
        self.content = content
        self.timestamp = date.today()

    def __str__(self):
        return f'Remetente: {self.sender}\n'\
               f'Destinatário: {self.receiver}\n' \
               f'Enviado em: {self.timestamp}\n' \
               f'Mensagem: {self.content}\n'

