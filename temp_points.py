from flask import Blueprint, jsonify
import os


temp_points = Blueprint('temp_points', __name__, url_prefix='/temp')


@temp_points.route("/getMentors", methods=["GET"])
def get_Mentors():
    path = "/home/images/mentors/"
    files = ["/temp/getMentor/" + f for f in os.listdir(path) if os.path.isfile(path + f)]
    return jsonify({"links_images": files})

