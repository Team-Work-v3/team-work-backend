from flask import Blueprint, jsonify, request
from events import LibraryDB

api_get = Blueprint('api_get', __name__, url_prefix='/api')

@api_get.route("/getEvents", methods=["GET"])
def get_events():
    db = LibraryDB()

    if 'id' in request.args:
        event_id = request.args['id']
        if not event_id.isdigit():
            return { "message": "error" }

        row = db.cursor.execute('''
            SELECT event_id, name_event, info, date, time, location,
                   max_places, price, category, image, is_active, created_by
            FROM events
            WHERE event_id = ?
        ''', (int(event_id),)).fetchone()

        if not row:
            return { "message": "error" }

        return {
            "events": [{
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
            }]
        }

    rows = db.cursor.execute('''
        SELECT event_id, name_event, info, date, time, location,
               max_places, price, category, image, is_active, created_by
        FROM events
    ''').fetchall()

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

    return { "events": result }