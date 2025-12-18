from flask import Blueprint, jsonify



temp_points = Blueprint('temp_points', __name__, url_prefix='/temp')