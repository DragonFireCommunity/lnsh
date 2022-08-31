import flask
from flask_cors import CORS

import sqlite3
import random

app = flask.Flask(__name__)
CORS(app)
db = sqlite3.connect('database.db', check_same_thread=False)
cursor = db.cursor()

@app.route('/')
def index():
    return flask.render_template('index.html')

# route with arguments
@app.route('/<code>')
def redirect(code):
    try:
        cursor.execute('SELECT url FROM urls WHERE code=?', (code,))
        urlFromCode = cursor.fetchone()[0]
    except:
        return "Error: Code not found"

    redirectURL = urlFromCode
    return flask.render_template('redirect.html', url = redirectURL)


@app.route('/api/shorten', methods = ['POST'])
def shorten():
    # generate random code (max length of 6)
    code = ''
    for i in range(6):
        code += str(random.randint(0, 9))
    # check if code already exists
    cursor.execute('SELECT code FROM urls WHERE code=?', (code,))
    if cursor.fetchone() is not None:
        # if code already exists, generate new code
        return shorten()
    # if code doesn't exist, insert into database
    url = flask.request.headers.get('url')
    cursor.execute('INSERT INTO urls (url, code) VALUES (?, ?)', (url, code))
    db.commit()
    return flask.jsonify(code=code)

app.run(debug=True)