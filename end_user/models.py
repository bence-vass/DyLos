from mongoengine import *



class EndUser(Document):
    foreign_user_id = StringField(required=True)
    service_preference = DictField()

