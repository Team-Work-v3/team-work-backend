from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from events import LibraryDB

api_post = Blueprint('api_post', __name__, url_prefix='/api')

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
