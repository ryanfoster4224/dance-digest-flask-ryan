from flask_mongoengine import MongoEngine
from mongoengine import *

connect(db="main",
        host='mongodb+srv://superadmin:rbDkYE2K4Qir69Om@dvas-cluster0.o1qow.mongodb.net/?retryWrites=true&w=majority',
        alias="default")

class Event(Document):
    title = StringField(max_length=50, required=True)
    price = StringField(max_length=12, default='невідомо')
    authorId = StringField(default="")
    full = StringField()
    brief = StringField()
    balance = StringField(default="merengue")
    location = StringField(default='локація невідома')
    start = StringField(max_length=5, default='07:00')
    weekdayId = IntField()
    weekday = StringField()
    published = BooleanField(default=False)

    meta = {"collection": "events"}


class User(Document):
    username = StringField(min_length=3, unique=True, required=True)
    hash = StringField(required=True)
    superAdmin = BooleanField(default=False)