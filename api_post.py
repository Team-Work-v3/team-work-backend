from flask import Blueprint, jsonify, request
from flask_login import current_user
from werkzeug.security import generate_password_hash, check_password_hash
from events import LibraryDB

api_post = Blueprint('api_post', __name__, url_prefix='/api')


@api_post.route("/checkAdmin", methods=["POST"])
def check_admin():
    data = request.get_json()
    if not False in [i in data.keys() and data[i] for i in ['login', 'password']]:
        user_in_db = LibraryDB().getUserByLogin(data['login'])
        if not user_in_db:
            return jsonify({'message': 'error', 'context': 'not found'})
        elif not check_password_hash(user_in_db[2], data['password']):
            return jsonify({'message': 'error', 'context': 'wrong password'})
        else:
            return jsonify({'message': 'success'})
    else:
        return jsonify({'message': 'error', 'context': 'missing fields'})


@api_post.route("/addEvents", methods=["POST"])
def add_event():
    data = request.get_json()
    if not False in [i in data.keys() and data[i] for i in ['name', 'date', 'number-of-seats', 'price',
                                                                    'category', 'img']]:
        LibraryDB().addEvent(data['name'], None, data['date'], data['time'],
                             '', data['number-of-seats'], data['price'], data['category'], data['img'], current_user[1])
        # ------------- заполнить по поступлению
    else:
        return jsonify({'message': 'error', 'context': 'missing fields'})
