from EmailAccount import EmailAccount


class BoxAccount:
    def __init__(self, email_account: EmailAccount):
        self.userData = email_account
        self.mailBox = []
