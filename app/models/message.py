import datetime
import json
from geojson import Point


message = {
        'message_id': 'ms-1wdjgsnju+3',
        'message_type': 'comment',
        'message_body': 'This football game is exciting',
        'timestamp': 1488928142.498821,
        'sentiment': {'attentiveness':1.5, ....},
        'loc': {'long': -73.974, 'lat': 40.764 },
    }



class Message:

    @staticmethod
    def message_from_dict_dated(map):
        message = Message(
            message_id=map['message_id'],
            message_type=map['message_type'],
            message_body=map['message_body'],
            timestamp =map['timestamp'],
            sentiment=map['sentiment']
        )
        return message

    def message_from_dict(map):
        if map['timestamp'] is not None:
            timestamp = map['timestamp']
        else:
            timestamp = datetime.datetime.now().time(),
        message = Message(
            message_id=map['message_id'],
            message_type=map['message_type'],
            message_body=map['message_body'],
            sentiment=map['sentiment'],
            timestamp=timestamp
            )
        return message

    def __init__(self,
                 message_id='',
                 message_type='',
                 message_body='',
                 timestamp=datetime.datetime.now().time(),
                 sentiment=''):
        self.message_id = message_id
        self.message_type = message_type
        self.message_body = message_body
        self.timestamp = timestamp
        self.sentiment = sentiment

    def __str__(self):
        return json.dumps(self.__dict__)

    def toJson(self):
        return self.__str__()

### not used below ###

# def message_decoder():
#     if '__type__' in map and map['__type__'] == 'Message':
#         message = Message(
#             message_id=map['message_id'],
#             name=map['name'],
#             start_time=map['start_time'],
#             duration=map['duration'],
#             senti_score=map['senti_score'],
#             host=map['host'],
#             host_user_id=map['host_user_id'],
#             location=map['location'],
#             location_id=map['location_id'],
#             facebook_id=map['facebook_id'],
#             attendees=map['attendees_id'],
#             keywords=map['keywords']
#         )
#     else:
#         raise Exception('dictionary has deficient fields')
#
# def test():
#     message = json.loads('{"__type__": "Evednt", "id": "evid", "name": "evn"}', object_hook=message_decoder)
#     message.hello()
#
# def test2():
#     evd = Message().__dict__
#     print(evd)
#
#
# if __name__ == '__main__':
#     test2()
