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

class GetObjFromDict:
    def __init__(self, d=None):
        if d is not None:
            for key, value in d.items():
                setattr(self, key, value)

@app.route('/')
def index():
    return app.send_static_file('index.html')


@app.route('/api/events')
def events_list():
    cursor = conn.cursor(DictCursor)
    try:
        rez = cursor.execute('SELECT * FROM parties')
    except:
        print('error while select')
    data = cursor.fetchall()
    print(data)
    cursor.close()

    return jsonify(data)


@app.route('/api/event/', methods=['POST'])
def event_insert():
    data = GetObjFromDict(request.json)
    print(data)
    cursor = conn.cursor(DictCursor)

    query =f'INSERT INTO parties (title, location, weekday, full, authorId, published ) VALUES ("{data.title}","{data.location}","{data.weekday}","{data.full}",{data.authorId},{data.published})'
    try:
        rez =  cursor.execute(query)
    except:
        print('error with '+query)
    finally:
        conn.commit()
        cursor.close()
        return jsonify({})


@app.route('/api/event/<int:id>', methods=['DELETE'])
def event_delete(id: int):
    print('deleting ' + str(id))
    cursor = conn.cursor(DictCursor)

    query = f'DELETE FROM parties WHERE id={id}'
    try:
        rez =  cursor.execute(query)
    except:
        print('deleting error '+ query)
    finally:
        conn.commit()
        cursor.close()
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
    print(request.json)
    return jsonify({})


if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
