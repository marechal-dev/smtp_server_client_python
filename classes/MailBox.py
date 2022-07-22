from classes.EmailAccount import EmailAccount
from classes.Email import Email


class MailBox:
    def __init__(self, email_account: EmailAccount):
        self.userData = email_account
        self.mailBox: [Email] = []
