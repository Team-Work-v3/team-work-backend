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
    return jsonify({"events": result})
