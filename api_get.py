from flask import Blueprint, jsonify, request
from events import LibraryDB

api_get = Blueprint('api_get', __name__, url_prefix='/api')