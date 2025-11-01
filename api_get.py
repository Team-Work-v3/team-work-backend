from flask import Blueprint
from flask_login import login_required, current_user
from events import LibraryDB

api_get = Blueprint('api_get', __name__, url_prefix='/api')

@api_get.route("/getEvents", methods=["GET"])
@login_required
def get_events():
    db = LibraryDB()
    user_id = current_user.id

    rows = db.cursor.execute('''
        SELECT event_id, name_event, info, date, time, location,
               max_places, price, category, image, is_active, created_by
        FROM events
        WHERE created_by = ?
    ''', (user_id,)).fetchall()

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
