class Key:
    def __init__(self, jwt):
        self.jwt = jwt

    def to_json(self):
        return self.__dict__
