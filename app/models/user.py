import json

class User:

    @staticmethod
    def user_from_dict(map):
        usr = User(
            fb_id=map['fb_id']
        )
        return usr

    def __init__(self,
                 fb_id = 0):
        self.fb_id = fb_id

    def __str__(self):
        return json.dumps(self.__dict__)

    def toJson(self):
        return self.__str__()