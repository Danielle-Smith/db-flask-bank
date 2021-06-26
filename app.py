from flask import Flask, jsonify, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import marshmallow_sqlalchemy
import os

app = Flask(__name__)

app.config['SECRET_KEY'] = ""
app.config['SQLALCHEMY_DATABASE_URI'] = ""
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25))
    amount = db.Column(db.Float)

    def __init__(self, name, amount):
        self.name = name
        self.amount = amount


class UserSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "amount")


user_schema = UserSchema()
users_schema = UserSchema(many=True)


@app.route('/users', methods=['GET'])
def get_users():
    all_users = User.query.all()
    result = users_schema.dump(all_users)
    return jsonify(result)


@app.route('/add-user', methods=['POST'])
def add_user():
    rqt = request.get_json(force=True)
    name = rqt["name"]
    amount = rqt["amount"]

    record = User(name, amount)
    db.session.add(record)
    db.session.commit()

    user = User.query.get(record.id)
    flash("User Added")
    return user_schema.jsonify(user)


@app.route('/user/<id>', methods=["GET"])
def get_user(id):
    user = User.query.get(id)
    result = user_schema.dump(user)
    return result


@app.route('/user-update/<id>', methods=['PATCH'])
def user_update(id):
    user = User.query.get(id)
    rqt = request.get_json(force=True)

    new_amount = rqt["amount"]
    user.amount = new_amount

    db.session.commit()
    print(user_schema.jsonify(user))
    return user_schema.jsonify(user)


@app.route('/delete-user/<id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.filter_by(id=id).first()
    db.session.delete(user)
    db.session.commit()
    return jsonify('user deleted')


if __name__ == '__main__':
    app.run()
