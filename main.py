from flask import Flask, jsonify, request
import os, hashlib
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor

app = Flask(__name__, static_url_path='/static')

mysql = MySQL()
app.config['MYSQL_DATABASE_HOST'] = os.getenv('MYSQL_DATABASE_HOST')
app.config['MYSQL_DATABASE_DB'] = os.getenv('MYSQL_DATABASE_DB')
app.config['MYSQL_DATABASE_USER'] = os.getenv('MYSQL_DATABASE_USER')
app.config['MYSQL_DATABASE_PASSWORD'] = os.getenv('MYSQL_DATABASE_PASSWORD')
app.config['MYSQL_DATABASE_PORT'] = int(os.getenv('MYSQL_DATABASE_PORT'))
mysql.init_app(app)
conn = mysql.connect()


@app.route('/')
def index():
    return app.send_static_file('index.html')


@app.route('/api/events')
def events_list():
    cursor = conn.cursor(DictCursor)

    rez = cursor.execute('SELECT * FROM parties')
    data = cursor.fetchall()
    print(data)
    cursor.close()

    return jsonify(data)


@app.route('/api/event/', methods=['POST'])
def event_add():
    print('adding ')
    return jsonify('maybe')


@app.route('/api/event/<int:id>', methods=['DELETE'])
def event_delete(id: int):
    print('deleting ' + str(id))
    return jsonify('maybe')


@app.route('/api/user/')
def get_permissions():
    username = request.args.get('username', type=str)
    password = request.args.get('password', type=str)

    if len(username) < 3 or len(password) < 3:
        return jsonify({'authorId': -1, 'superAdmin': False})
    hash = ("SHA-256:", hashlib.sha256(password.encode()).hexdigest())[1]

    cursor = conn.cursor(DictCursor)
    rez = cursor.execute(f'SELECT authorId, hash, superAdmin FROM users WHERE username="{username}"')  # TODO: sanitize
    data = cursor.fetchone()

    if not data:
        return jsonify({'authorId': -1, 'superAdmin': False})

    print(data)
    if data['hash'] == hash:
        return jsonify({'authorId': data['authorId'], 'superAdmin': bool(data['superAdmin'])})

    cursor.close()

    print(username, hash)
    return jsonify({'authorId': 100, 'superAdmin': False})


@app.route('/api/user', methods=['POST'])
def user_create():
    pass


if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
