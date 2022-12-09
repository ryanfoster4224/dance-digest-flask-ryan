from flask import Flask, jsonify, request
import os, hashlib
from dotenv import load_dotenv
from flask_mongoengine import MongoEngine
from mongoengine import *
import hashlib
from bson.objectid import ObjectId
import datetime

load_dotenv()  # take environment variables from .env.

app = Flask(__name__, static_url_path='/static')

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
    location = StringField(default='АТБ на Виноградарі')
    start = StringField(max_length=5, default='07:00')
    weekdayId = IntField()
    weekday = StringField()
    published = BooleanField(default=False)

    meta = {"collection": "events"}


class User(Document):
    username = StringField(min_length=3, unique=True, required=True)
    hash = StringField(required=True)
    superAdmin = BooleanField(default=False)


@app.route('/api/events')
def events_list():
    weekday_id = datetime.datetime.today().weekday()
    return Event.objects(weekdayId__gte=weekday_id)\
        .order_by('weekdayId').to_json()


@app.route('/api/event', methods=['POST'])
def event_add():
    body = request.json
    print(body)
    event = Event(**body)
        # title=body['title'],
        # price=body['price'],
        # authorId=body['authorId'],
        # full=body['full'],
        # brief=body.get('brief', None),
        # published=body['published'],
        # balance=body['balance'],
        # weekdayId=body.get('weekdayId', -1),
        # weekday=body.get('weekday', None),
        # start=body.get('start', None),
        # location=body.get('location', None)

    event.save()
    return {"status": "added"}


@app.route('/api/event', methods=['PUT'])
def event_update():
    body = request.json
    print(body)
    try:
        Event.objects(pk=body['id']) \
            .update(**body)
    except:
        return jsonify({"status": "error on update"})

    return jsonify({"status": "updated"})


@app.route('/api/event/<string:sid>', methods=['DELETE'])
def event_delete(sid: str):
    print('deleting ' + (sid))

    try:
        de = Event.objects(pk=sid).first()
        print(type(de), de.id)
        de.delete()
    except:
        print('deleting error')
        return jsonify({"status": "deleting error"})

    return jsonify({"status": "deleted sucessfully"})


@app.route('/api/user/')
def get_permissions():
    username = request.args.get('username', type=str)
    password = request.args.get('password', type=str)

    if len(username) < 3 or len(password) < 3:
        return jsonify({'authorId': "", 'superAdmin': False})
    hash = ("SHA-256:", hashlib.sha256(password.encode()).hexdigest())[1]
    try:
        user = User.objects(username=username).first()
    except:
        return jsonify({'authorId': "", 'superAdmin': False})

    if user:
        print(type(user))
        print(type(user.pk), type(user.superAdmin))
        print(user.pk, user.superAdmin)
        if user.hash == hash:
            # return jsonify("maybe")
            return jsonify({'authorId': str(user.pk), 'superAdmin': bool(user.superAdmin)})

    else:
        return jsonify({'authorId': "", 'superAdmin': False})


@app.route('/api/user', methods=['POST'])
def user_add():
    body = request.json
    if len(body['password']) < 3:
        return "too short password"
    # encode it to bytes using UTF-8 encoding
    body['hash'] = ("SHA-256:", hashlib.sha256(body['password'].encode()).hexdigest())[1]
    # body['hash'] = 'fsdfsdf'

    print(body)
    user = User(username=body['username'], hash=body['hash'])
    user.save()
    return {"status": "user created"}


@app.route('/add')
def add():
    e1 = Event(title='java conference')
    e1.save()
    return [{"status": "added"}]


@app.route('/')
def index():
    return app.send_static_file('index.html')


if __name__ == '__main__':
    # user = User.objects(username='cherk').first()

    app.run(debug=True, port=os.getenv("PORT", default=5000))
