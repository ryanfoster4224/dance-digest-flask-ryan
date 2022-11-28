from flask import Flask, jsonify
import os
from dotenv import load_dotenv, dotenv_values
load_dotenv()  # take environment variables from .env.

from flaskext.mysql import MySQL
mysql = MySQL()

app = Flask(__name__)
app.config['MYSQL_DATABASE_HOST'] = os.getenv('MYSQL_DATABASE_HOST')
app.config['MYSQL_DATABASE_DB'] = os.getenv('MYSQL_DATABASE_DB')
app.config['MYSQL_DATABASE_USER'] = os.getenv('MYSQL_DATABASE_USER')
app.config['MYSQL_DATABASE_PASSWORD'] = os.getenv('MYSQL_DATABASE_PASSWORD')
app.config['MYSQL_DATABASE_PORT'] = int(os.getenv('MYSQL_DATABASE_PORT'))

mysql.init_app(app)
conn = mysql.connect()
cursor = conn.cursor()

rez = cursor.execute('SELECT * FROM test2')
data = cursor.fetchall()

print(data)
cursor.close()


@app.route('/')
def index():
    return jsonify(data)
    # return jsonify({"Choo Choo": "Welcome to dance-digest Flask"})


if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
