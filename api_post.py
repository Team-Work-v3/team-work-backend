from flask import Blueprint, jsonify, request
from dbToDO import DataBase

api_post = Blueprint('api_post', __name__, url_prefix='/post')