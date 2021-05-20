class Discount:
    def __init__(self, gama_produs, procent, data_expirare):
        self.gama_produs = gama_produs
        self.procent = procent
        self.data_expirare = data_expirare

    def to_json(self):
        return self.__dict__
