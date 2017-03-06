import datetime
import json
from bson import ObjectId


class Event:

    @staticmethod
    def event_from_dict(map):
        event = Event(
            event_id=map['event_id'],
            name=map['name'],
            start_time=map['start_time'],
            duration=map['duration'],
            senti_score=map['senti_score'],
            host=map['host'],
            host_user_id=map['host_user_id'],
            location=map['location'],
            location_id=map['location_id'],
            facebook_id=map['facebook_id'],
            attendees=map['attendees'],
            keywords=map['keywords']
        )
        return event

    def __init__(self,
                 event_id=0,
                 name='',
                 start_time='',
                 duration='',
                 senti_score='',
                 host='',
                 host_user_id='',
                 location='',
                 location_id='',
                 facebook_id='',
                 attendees='',
                 keywords=''):
        self.event_id = event_id
        self.name = name
        self.start_time = start_time
        self.duration = duration
        self.senti_score = senti_score
        self.host = host
        self.host_user_id = host_user_id
        self.location = location
        self.location_id = location_id
        self.facebook_id = facebook_id
        self.attendees = attendees
        self.keywords = keywords

    def __str__(self):
        return json.dumps(self.__dict__)

### not used below ###

# def event_decoder():
#     if '__type__' in map and map['__type__'] == 'Event':
#         event = Event(
#             event_id=map['event_id'],
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
#     event = json.loads('{"__type__": "Evednt", "id": "evid", "name": "evn"}', object_hook=event_decoder)
#     event.hello()
#
# def test2():
#     evd = Event().__dict__
#     print(evd)
#
#
# if __name__ == '__main__':
#     test2()
