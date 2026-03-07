from flask import Flask, render_template, request, redirect, send_file
from werkzeug.security import check_password_hash
from flask_login import LoginManager, login_user, login_required, current_user, logout_user
import logging
from logging.handlers import RotatingFileHandler
from pydantic import ValidationError

from user_class import User
from events import LibraryDB
from api_post import api_post
from api_get import api_get
from temp_points import temp_points
from utils import RegModel

www_path = 'www'
app = Flask(__name__, static_folder=www_path, static_url_path="", template_folder=www_path)
app.config["SECRET_KEY"] = "o8pjag5ny;o32g42vonny8libtfukjyj,gyukfyfkufyulgyuk"
werkzeug_logger = logging.getLogger('werkzeug')
werkzeug_logger.addHandler(RotatingFileHandler('logs.log', maxBytes=10*1024*1024))
werkzeug_logger.addHandler(logging.StreamHandler())

login_manager = LoginManager(app)
login_manager.login_view = 'admin_login'

rules_to_remove = []

for rule in app.url_map.iter_rules():
    if rule.endpoint == "static" and rule.rule.endswith(".html"):
        rules_to_remove.append(rule)

for rule in rules_to_remove:
    app.url_map._rules.remove(rule)
    app.url_map._rules_by_endpoint["static"].remove(rule)


app.register_blueprint(api_get)
app.register_blueprint(api_post)
app.register_blueprint(temp_points)

@login_manager.user_loader
def load_user(user_id):
    return User(user_id, LibraryDB())


@app.route("/admin", methods=['GET'])
@login_required
def admin():
    return render_template("admin/events.html")


@app.route("/admin/login", methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        try:
            user_data = RegModel(**request.form)
            user_in_db = LibraryDB().getUserByLogin(user_data.login)
            if not user_in_db:
                return render_template("login.html", errors=True)
            elif not check_password_hash(user_in_db[2], user_data.password):
                return render_template("login.html", errors=True)
            else:
                user_to_login = User(db_user=user_in_db)
                remember = 'device' in request.form.keys()
                login_user(user_to_login, remember=remember)
                return redirect("/admin")
        except ValidationError:
            return render_template("login.html", errors=True)
    return render_template("login.html", errors=False)


@app.route("/admin/logout", methods=['GET'])
@login_required
def admin_logout():
    logout_user()
    return redirect('/admin/login')


@app.route("/admin/events", methods=['GET'])
@login_required
def admin_events():
    return render_template("admin/events.html")


@app.route("/admin/analitic", methods=['GET'])
@login_required
def admin_analitic():
    return render_template("admin/analitic.html")


@app.route("/admin/members", methods=['GET'])
@login_required
def admin_members():
    return render_template("admin/members.html")


@app.route("/admin/other", methods=['GET'])
@login_required
def admin_other():
    return render_template("admin/other.html")

@app.route("/")
@app.route("/index")
@app.route("/event/<eid>")
def index(eid=''):
    return render_template("index/index.html")

@app.route("/admin/change-event/<eid>")
def change_event(eid):
    return render_template("admin/change-event.html", event_id=eid)

@app.route("/images/<name>")
def prev_photo(name):
    return send_file(f"/home/images/{name}")

@app.route("/<path:filepath>.html")
@login_required
def html_router(filepath):
    template_name = f"{filepath}.html"
    return render_template(template_name)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
