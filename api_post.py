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
            "description_event": row[2],
            "date_event": row[3],
            "time_event": row[4],
            "location_event": row[5],
            "seats_event": row[6],
            "price_event": row[7],
            "event_category": row[8],
            "images_events": row[9],
            "organizers_event": row[10],
            "program_event": row[11],
            "fullDescription_event": row[12],
            "is_active": row[13],
            "created_by": row[14]
        })
    else:
        return jsonify({'message': 'error', 'context': 'missing fields'})


@api_post.route("/addEvents", methods=["POST"])
@login_required
def add_event():
    data = request.get_json()
    to_check = [
        ('name_event', str), ('date_event', str), ('seats_event', int),
        ('price_event', float), ('event_category', str), ('images_events', str)
    ]
    if validate_greedy(to_check, data):
        LibraryDB().addEvent(
            data['name_event'],
            data.get('description_event'),
            data['date_event'],
            data['time_event'],
            data.get('location_event', ''),
            data['seats_event'],
            data['price_event'],
            data['event_category'],
            data['images_events'],
            data.get('organizers_event', ''),
            data.get('program_event', ''),
            data.get('fullDescription_event', ''),
            current_user.user[0],
            True
        )
        return jsonify({'message': 'success'})
    else:
        return jsonify({'message': 'error', 'context': 'missing fields'})


@api_post.route("/editEvents", methods=["POST"])
@login_required
def edit_event():
    data = request.get_json()
    to_check = [
        ('event_id', int), ('name_event', str), ('date_event', str),
        ('seats_event', int), ('price_event', float),
        ('event_category', str), ('images_events', str)
    ]
    if validate_greedy(to_check, data, False):
        LibraryDB().updateEvent(
            data['event_id'],
            data['name_event'],
            data.get('description_event'),
            data['date_event'],
            data['time_event'],
            data.get('location_event'),
            data['seats_event'],
            data['price_event'],
            data['event_category'],
            data['images_events'],
            data.get('organizers_event'),
            data.get('program_event'),
            data.get('fullDescription_event'),
            current_user.user[0],
            data.get('is_active')
        )
        return jsonify({'message': 'success'})
    else:
        return jsonify({'message': 'error', 'context': 'missing fields'})


@api_post.route("/deleteEvent", methods=["POST"])
@login_required
def delete_event():
    data = request.get_json()
    if not data or "event_id" not in data:
        return jsonify({"message": "error", "context": "missing event_id"})
    LibraryDB().deleteEvent(data["event_id"])
    return jsonify({"message": "success"})


@api_post.route("/addEventsForm", methods=["POST"])
@login_required
def add_events():
    data = request.form.to_dict()
    print(data)
    print()
    """
    LibraryDB().addEvent(
        request.form["name_event"],
        request.form["description_event"],
        request.form["date_event"],
        request.form["time_event"],
        request.form["location_event"],
        request.form["seats_event"],
        request.form["price_event"],
        request.form["event_category"],
        request.form["images_events"],
        request.form["organizers_event"],
        request.form["program_event"],
        request.form["fullDescription_event"],
        current_user.user[0],
        True
    )"""
    return {"message": "success"}


@api_post.route("/editEventsForm", methods=["POST"])
@login_required
def edit_events():
    LibraryDB().updateEvent(
        int(request.form.get("event_id")),
        request.form.get("name_event"),
        request.form.get("description_event"),
        request.form.get("date_event"),
        request.form.get("time_event"),
        request.form.get("location_event"),
        int(request.form.get("seats_event")),
        float(request.form.get("price_event")),
        request.form.get("event_category"),
        request.form.get("images_events"),
        request.form.get("organizers_event"),
        request.form.get("program_event"),
        request.form.get("fullDescription_event"),
        current_user.user[0],
        request.form.get("is_active")
    )
    return {"message": "success"}
