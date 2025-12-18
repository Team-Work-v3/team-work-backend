from flask import Blueprint, jsonify, send_file
import os


temp_points = Blueprint('temp_points', __name__, url_prefix='/temp')


@temp_points.route("/getMentors", methods=["GET"])
def get_Mentors():
    path = "/home/images/mentors/"
    files = ["/temp/getMentor/" + f for f in os.listdir(path) if os.path.isfile(path + f)]
    return jsonify({"links_images": files})

@temp_points.route("/getMentor/<filelink>", methods=["GET"])
def get_Mentor(filelink):
    print(filelink)
    path = "/home/images/mentors/" + filelink
    print(path)
    return send_file(path, as_attachment=True)