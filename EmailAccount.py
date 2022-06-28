class EmailAccount:
    def __init__(self, name: str, username: str, domain: str, password: str):
        self.name = name
        self.username = username
        self.address = f'{username}{domain}'
        self.password = password
