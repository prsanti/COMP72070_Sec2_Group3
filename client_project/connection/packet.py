import json

class Packet:
    def __init__(self, type, category, data):
        self.type = type
        self.category = category
        self.data = data

    def serialize(self):
        packet_dict = {
            'type': self.type.name,
            'category': self.category.name,
            'data': self.data
        }
        return json.dumps(packet_dict).encode() 