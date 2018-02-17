from flask import Flask, request, Response, jsonify
from flask_cors import cross_origin
import http.client
from auth import tokens
from auth import models
from auth.models import db
from sqlalchemy.exc import IntegrityError


app = Flask(__name__)


@app.route('/tokens', methods=['POST'])
@cross_origin(headers=['Content-Type'])
def authorize():
    grant_type = request.json['grant_type']
    if grant_type != 'password':
        raise NotImplemented()

    acc = models.Account.query.filter_by(
        email=request.json['email'],
        password=request.json['password'],
    ).first()

    if acc is None:
        return Response(status=http.client.UNAUTHORIZED)

    token_builder = tokens.B2CTokenBuilder(acc.account_id)
    access_token = token_builder.issue_access_token()

    return jsonify(
        account_id=acc.account_id,
        access_token=access_token.data,
        expires_in=access_token.expires_in,
    )


@app.route('/accounts', methods=['POST'])
@cross_origin(headers=['Content-Type'])
def register():
    try:
        acc = models.Account(
            email=request.json['email'],
            password=request.json['password']
        )

        db.session.add(acc)
        db.session.commit()
    except IntegrityError:
        return Response(status=http.client.CONFLICT)

    resp = jsonify(account_id=acc.account_id)
    return Response(resp.response, http.client.CREATED)


# TODO: pagination
@app.route('/accounts', methods=['GET'])
def get_all():
    accounts = [{
        'account_id': a.account_id,
        'email': a.email,
    } for a in models.Account.query.all()]

    return jsonify(accounts=accounts)


if __name__ == '__main__':
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
    app.config['SQLALCHEMY_ECHO'] = True
    db.init_app(app)
    db.app = app
    db.create_all()
    app.run('0.0.0.0', 8080, debug=True)
