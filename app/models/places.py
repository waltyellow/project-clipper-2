import datetime
import json
from bson import ObjectId


class Places:

    @staticmethod
    def places_from_dict(map):
        loc = Places(
            places_id=map['location_id'],
            geo_coordinate = map['geo_coordinate'],
            senti_score=map['senti_score'],
            location_type=map['location_type'],
            keywords=map['keywords']
        )
        return loc


    def __init__(self,
                 location_id=0,
                 geo_coordinate='',
                 senti_score='',
                 location_type='',
                 keywords=''
                 ):
        self.places_id = location_id
        self.geo_coordinate = geo_coordinate
        self.senti_score = senti_score
        self.location_type = location_type
        self.keywords = keywords


    def __str__(self):
        return json.dumps(self.__dict__)

    def toJson(self):
        return self.__str__()