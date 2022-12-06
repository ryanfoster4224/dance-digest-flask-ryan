from flask import Flask, jsonify, request
import os, hashlib
from dotenv import load_dotenv
from flask_mongoengine import MongoEngine
from mongoengine import *
import hashlib


load_dotenv()  # take environment variables from .env.

app = Flask(__name__, static_url_path='/static')
# app.config['MONGODB_SETTINGS'] =  {
#     "DB": "main",
#     "host":'mongodb+srv://superadmin:rbDkYE2K4Qir69Om@dvas-cluster0.o1qow.mongodb.net/?retryWrites=true&w=majority',
#     "alias":"default"
# }

connect(db = "main", host = 'mongodb+srv://superadmin:rbDkYE2K4Qir69Om@dvas-cluster0.o1qow.mongodb.net/?retryWrites=true&w=majority',
    alias = "default")

class Event(Document):
    title = StringField(max_length=50, required=True)
    price = StringField(max_length=12)

    meta = {"collection":"events"}

class InputUser(Document):
    username = StringField(min_length=3, required=True)
    password = StringField(required=True)
    superAdmin = BooleanField(default=False)

class User(Document):
    username = StringField(min_length=3, required=True)
    hash = StringField(required=True)
    superAdmin = BooleanField(default=False)


@app.route('/api/events')
def events_list():
    return Event.objects.to_json()

@app.route('/api/event', methods = ['POST'])
def event_add():
    body = request.json
    print(body)
    event = Event(title = body['title'], price = body['price'])
    event.save()
    return {"hello":"world"}

@app.route('/api/user', methods = ['POST'])
def user_add():
    body = request.json
    # encode it to bytes using UTF-8 encoding
    body['hash'] = ("SHA-256:", hashlib.sha256(body['password'].encode()).hexdigest())[1]
    # body['hash'] = 'fsdfsdf'

    print(body)
    user = User(username = body['username'], hash = body['hash'])
    user.save()
    return {"status":"user created"}


@app.route('/add')
def add():
    e1 = Event(title='java conference')
    e1.save()
    return [{"status":"added"}]

@app.route('/')
def index():
    return app.send_static_file('index.html')

if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))

