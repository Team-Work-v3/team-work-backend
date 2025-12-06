from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user, login_user
from werkzeug.security import check_password_hash
from events import LibraryDB
from user_class import User
from utils import validate_greedy

api_post = Blueprint('api_post', __name__, url_prefix='/api')


@api_post.route("/checkAdmin", methods=["POST"])
def check_admin():
    data = request.get_json()
    to_check = [('login', str), ('password', str)]
    if validate_greedy(to_check, data):
        user_in_db = LibraryDB().getUserByLogin(data['login'])
        if not user_in_db:
            return jsonify({'message': 'error', 'context': 'not found'})
        elif not check_password_hash(user_in_db[2], data['password']):
            return jsonify({'message': 'error', 'context': 'wrong password'})
        else:
            user_to_login = User(db_user=user_in_db)
            remember = 'device' in request.form.keys()
            login_user(user_to_login, remember=remember)
            return jsonify({'message': 'success'})
    else:
        return jsonify({'message': 'error', 'context': 'missing fields'})


@api_post.route("/getEvent", methods=["POST"])
def get_event():
    data = request.get_json()
    to_check = [('id', int)]
    if validate_greedy(to_check, data, False):
        row = LibraryDB().getEvent(data['id'])
        if not row:
            return jsonify({'message': 'error', 'context': 'not found'})
        return jsonify({
            "event_id": row[0],
            "name_event": row[1],
            "info": row[2],
            "date": row[3],
            "time": row[4],
            "location": row[5],
            "max_places": row[6],
            "price": row[7],
            "category": row[8],
            "image": row[9],
            "is_active": row[10],
            "created_by": row[11]
        })
    else:
        return jsonify({'message': 'error', 'context': 'missing fields'})


@api_post.route("/addEvents", methods=["POST"])
@login_required
def add_event():
    data = request.get_json()
    to_check = [('name', str), ('date', str), ('number-of-seats', int), ('price', float), ('category', str), ('img', str)]
    if validate_greedy(to_check, data):
        LibraryDB().addEvent(data['name'], None, data['date'], data['time'],
                             '', data['number-of-seats'], data['price'], data['category'],
                             data['img'], current_user.user[1])
        # ------------- заполнить по поступлению
        return jsonify({'message': 'success'})
    else:
        return jsonify({'message': 'error', 'context': 'missing fields'})


@api_post.route("/editEvents", methods=["POST"])
@login_required
def edit_event():
    data = request.get_json()
    to_check = [('name', str), ('date', str), ('number-of-seats', int), ('price', float), ('category', str), ('img', str)]
    if validate_greedy(to_check, data, False):
        LibraryDB().updateEvent('id......', data['name'], None, data['date'], data['time'],
                             '', data['number-of-seats'], data['price'], data['category'], data['img'], current_user[1])
        # ------------- исправить по поступлению
        return jsonify({'message': 'success'})
    else:
        return jsonify({'message': 'error', 'context': 'missing fields'})


@api_post.route("/addEvents", methods=["POST"])
@login_required
def add_events():
    LibraryDB().addEvent(
        request.form.get("name_event"),
        request.form.get("info"),
        request.form.get("date"),
        request.form.get("time"),
        request.form.get("location"),
        request.form.get("max_places"),
        request.form.get("price"),
        request.form.get("category"),
        request.form.get("image"),
        current_user.user[0],
        True
    )
    return {"message": "success"}

@api_post.route("/editEvents", methods=["POST"])
@login_required
def edit_events():
    LibraryDB().updateEvent(
        request.form.get("event_id"),
        request.form.get("name_event"),
        request.form.get("info"),
        request.form.get("date"),
        request.form.get("time"),
        request.form.get("location"),
        request.form.get("max_places"),
        request.form.get("price"),
        request.form.get("category"),
        request.form.get("image"),
        request.form.get("is_active")
    )
    return {"message": "success"}
