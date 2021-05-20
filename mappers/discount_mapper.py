from models.discount import Discount


def from_json_to_object(json):
    gama_produs = json["gama_produs"]
    procent = json["procent"]
    data_expirare = json["data_expirare"]

    return Discount(gama_produs, procent, data_expirare)
