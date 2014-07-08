from flask import Flask, request, Response, jsonify
from flask_sqlite import SQLite3
from flask_cors import cross_origin
import http.client
import tokens


app = Flask(__name__)
db = SQLite3(app)


def init_db(conn):
    conn.execute(
        'CREATE TABLE IF NOT EXISTS accounts'
        '(account_id INTEGER PRIMARY KEY, email UNIQUE, password)')


@app.route('/tokens', methods=['POST'])
@cross_origin(headers=['Content-Type'])
def authorize():
    grant_type = request.json['grant_type']
    if grant_type != 'password':
        raise NotImplemented()

    email = request.json['email']
    password = request.json['password']

    with db.connection as tr:
        cur = tr.cursor()

        cur.execute(
            'SELECT account_id FROM accounts '
            'WHERE email=? AND password=?',
            (email, password))

        acc = cur.fetchone()

        if acc is None:
            return Response(status=http.client.UNAUTHORIZED)

        token_builder = tokens.B2CTokenBuilder(acc[0])
        access_token = token_builder.issue_access_token()

        return jsonify(
            account_id=acc[0],
            access_token=access_token.data,
            expires_in=access_token.expires_in,
        )


@app.route('/accounts', methods=['POST'])
@cross_origin(headers=['Content-Type'])
def register():
    email = request.json['email']
    password = request.json['password']
    with db.connection as tr:
        cur = tr.cursor()
        cur.execute(
            'INSERT INTO accounts(email, password) '
            'VALUES(?, ?)', (email, password))

        resp = jsonify(account_id=cur.lastrowid)
        return Response(resp.response, http.client.CREATED)


@app.route('/accounts', methods=['GET'])
def get_all():
    with db.connection as tr:
        cur = tr.cursor()
        cur.execute('SELECT * FROM accounts')

        accounts = map(lambda r: dict(
            account_id=r[0],
            email=r[1],
            password=r[2],
        ), cur.fetchall())

    return jsonify(accounts=list(accounts))


if __name__ == '__main__':
    import sqlite3
    cs = 'file:auth?mode=memory&cache=shared'
    memdb = sqlite3.connect(cs)
    init_db(memdb)

    app.config.setdefault('DATABASE', cs)
    app.run('0.0.0.0', 8080, debug=True)
