from flask import Blueprint, jsonify, request
from dbToDO import DataBase

api_get = Blueprint('api_get', __name__, url_prefix='/get')