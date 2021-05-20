from utils.json_encoder import encode


class DiscountEnhanced:
    def __init__(self, discount, _id):
        self.id = _id
        self.discount = discount

    def to_json(self):
        final_json = {
            "_id": encode(self.id),
            "gama_produs": self.discount.gama_produs,
            "procent": self.discount.procent,
            "data_expirare": self.discount.data_expirare,

        }

        final_json["_id"] = final_json["_id"][1:-1]

        return final_json
