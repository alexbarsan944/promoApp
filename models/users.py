class User:
    def __init__(self, name, email, password, discounts):
        self.name = name
        self.email = email
        self.password = password
        self.discounts = discounts

    def to_json(self):
        return self.__dict__
