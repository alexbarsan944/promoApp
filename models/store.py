class Store:
    def __init__(self, store_name, password, email):
        self.store_name = store_name
        self.password = password
        self.email = email

    def to_json(self):
        return self.__dict__
