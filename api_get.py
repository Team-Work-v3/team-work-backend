from flask import Blueprint, jsonify
from flask_login import login_required
from events import LibraryDB

api_get = Blueprint('api_get', __name__, url_prefix='/api')

@api_get.route("/getEvents", methods=["GET"])
def get_events():
    rows = LibraryDB().getEvents()
    result = []
    for row in rows:
        result.append({
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
    return jsonify({"events": result})


@api_get.route("/getShortenedEvents", methods=["GET"])
def get_shortened_events():
    rows = LibraryDB().getEvents()
    result = []
    for row in rows:
        result.append({
            "event_id": row[0],
            "name_event": row[1],
            "date_event": row[3],
            "time_event": row[4],
            "price_event": row[7],
            "event_category": row[8],
            "images_events": row[9],
            "is_active": row[13],
        })
    return jsonify({"events": result})


@api_get.route("/getUsers", methods=["GET"])
def get_users():
    rows = LibraryDB().getRegistrations()
    result = []
    for row in rows:
        result.append({
            "id_event": row[1],
            "full_name": row[2],
            'email': row[3],
            'phone_number': row[4],
            'agreement': row[5]
        })
    return jsonify({"events": result})

@api_get.route("/getUsersInEvents", methods=["GET"])
def get_users_in_events():
    events = LibraryDB().getEvents()
    result = []

    for event in events:
        event_id = event[0]
        event_name = event[1]

        users = LibraryDB().cursor.execute(
            "SELECT full_name, email, phone_number, agreement FROM registration WHERE id_event = ?",
            (event_id,)
        ).fetchall()

        users_list = []
        for u in users:
            users_list.append({
                "full_name": u[0],
                "email": u[1],
                "phone_number": u[2],
                "agreement": u[3]
            })

        result.append({
            "event_id": event_id,
            "event_name": event_name,
            "users": users_list
        })

    return jsonify({"events": result})
