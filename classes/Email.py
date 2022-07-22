from datetime import date


class Email:
    def __init__(self, receiver_address: str, sender_address: str, subject: str, content: str):
        self.receiver = receiver_address
        self.sender = sender_address
        self.subject = subject
        self.content = content
        self.timestamp = date.today()

    def __str__(self):
        return f'Remetente: {self.sender}\n' \
               f'Destinatário: {self.receiver}\n' \
               f'Assunto: {self.subject}\n' \
               f'Enviado em: {self.timestamp}\n' \
               f'Mensagem: {self.content}\n'
