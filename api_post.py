from flask import Blueprint, jsonify, request, redirect
from flask_login import login_required, current_user
from pydantic import ValidationError
import secrets
from events import LibraryDB
from utils import validate_greedy, EventGetModel, EventAddModel

api_post = Blueprint('api_post', __name__, url_prefix='/api')


@api_post.route("/getEvent", methods=["POST"])
def get_event():
    data = request.get_json()
    try:
        event_data = EventGetModel(**data)
        row = LibraryDB().getEvent(event_data.id)
        if not row:
            return jsonify({'message': 'error', 'context': 'not found'})
        event_id = row[0]
        seats_event = row[6]
        remaining = LibraryDB().calcRemainingSeats(event_id, seats_event)
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
            "created_by": row[14],
            "remaining_seats": remaining
        })
    except ValidationError:
        return jsonify({'message': 'error', 'context': 'bad fields'})


@api_post.route("/addEvents", methods=["POST"])
@login_required
def add_event():
    data = request.get_json()
    try:
        event_data = EventAddModel(**data)
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
    except ValidationError:
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
        return jsonify({"message": "error"})
    LibraryDB().deleteEvent(data["event_id"])
    return jsonify({"message": "success"})


@api_post.route("/addReview", methods=["POST"])
def add_review():
    data = request.get_json()
    to_check = [('id_registration', int), ('event_id', int), ('review_text', str)]

    if validate_greedy(to_check, data):
        LibraryDB().addReview(
            data['id_registration'],
            data['event_id'],
            data['review_text'],
            data['is_approved']
        )
        return jsonify({'message': 'success'})
    else:
        return jsonify({'message': 'error'})


@api_post.route("/regUser", methods=["POST"])
def reg_user():
    data = request.get_json()
    data['confirmation'] = 1
    to_check = [
        ('id_event', int), ('full_name', str), ('email', str),
        ('phone_number', str), ('agreement', int),
        ('ticket_amount', int), ('confirmation', int)
    ]
    if validate_greedy(to_check, data, True):
        LibraryDB().addRegistration(
            data['id_event'],
            data['full_name'],
            data['email'],
            data['phone_number'],
            data['agreement'],
            data['ticket_amount'],
            data['confirmation']
        )
        return jsonify({'message': 'success'})
    else:
        return jsonify({'message': 'error', 'context': 'missing fields'})


@api_post.route("/addEventsForm", methods=["POST"])
@login_required
def add_events():
    file = request.files['images-events']
    name = 'logoEvents.png'
    if file:
        name = f'{secrets.token_hex(16)}.{file.filename.split('.')[-1]}'
        while LibraryDB().getImageByName(name):
            name = f'{secrets.token_hex(16)}.{file.filename.split('.')[-1]}'
        file.save(f'/home/images/{name}')
    LibraryDB().addEvent(
        request.form['name_event'], request.form['description_event'],
        request.form['date_event'], request.form['time_event'], request.form['location_event'],
        request.form['seats_event'], request.form['price_event'], request.form['event_category'],
        f"/images/{name}", request.form['organizers_event'], request.form['program_event'],
        request.form['fullDescription_event'], 0
    )
    return redirect("/admin")


@api_post.route("/deleteRegistration", methods=["POST"])
@login_required
def delete_registration():
    data = request.get_json()

    if not data or "id_registration" not in data:
        return jsonify({"message": "error", "context": "missing fields"})

    result = LibraryDB().deleteRegistration(data["id_registration"])

    if result:
        return jsonify({"message": "success"})
    else:
        return jsonify({"message": "error"})


@api_post.route("/editEventsForm/<id>", methods=["POST"])
@login_required
def edit_events(id):
    file = request.files['images-events']
    name = 'logoEvents.png'
    if file:
        name = f'{secrets.token_hex(16)}.{file.filename.split('.')[-1]}'
        while LibraryDB().getImageByName(name):
            name = f'{secrets.token_hex(16)}.{file.filename.split('.')[-1]}'
        file.save(f'/home/images/{name}')
    LibraryDB().updateEvent(
        int(id), request.form['name_event'], request.form['description_event'],
        request.form['date_event'], request.form['time_event'], request.form['location_event'],
        request.form['seats_event'], request.form['price_event'], request.form['event_category'],
        f"/images/{name}", request.form['organizers_event'], request.form['program_event'],
        request.form['fullDescription_event'], 0
    )
    return redirect("/admin/events")


@api_post.route("/editRegistration", methods=["POST"])
@login_required
def edit_registration():
    data = request.get_json()

    to_check = [
        ('id_registration', int),
        ('full_name', str),
        ('email', str),
        ('phone_number', str),
        ('agreement', int),
        ('ticket_amount', int),
        ('confirmation', int)
    ]

    if validate_greedy(to_check, data, False):
        result = LibraryDB().updateRegistration(
            data['id_registration'],
            data['full_name'],
            data['email'],
            data['phone_number'],
            data['agreement'],
            data['ticket_amount'],
            data['confirmation']
        )

        if result:
            return jsonify({'message': 'success'})
        else:
            return jsonify({'message': 'error', 'context': 'not found'})
    else:
        return jsonify({'message': 'error', 'context': 'missing fields'})


@api_post.route("/deleteReview", methods=["POST"])
@login_required
def delete_review():
    data = request.get_json()

    if not data or "review_id" not in data:
        return jsonify({"message": "error"})

    result = LibraryDB().deleteReview(data["review_id"])

    if result:
        return jsonify({"message": "success"})
    else:
        return jsonify({"message": "error"})
