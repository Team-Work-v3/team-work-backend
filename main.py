from flask import Flask, render_template, request, redirect, flash
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.routing import Rule
from flask_login import LoginManager, login_user, login_required, current_user, logout_user
from user_class import User
from events import LibraryDB
from api_post import api_post
from api_get import api_get
from utils import validate_greedy

www_path = 'www'
app = Flask(__name__, static_folder=www_path, static_url_path="", template_folder=www_path)
app.config["SECRET_KEY"] = "o8pjag5ny;o32g42vonny8libtfukjyj,gyukfyfkufyulgyuk"
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


@login_manager.user_loader
def load_user(user_id):
    return User(user_id, LibraryDB())


@app.route("/admin", methods=['GET'])
@login_required
def admin():
    return render_template("admin/events.html")


@app.route("/admin/add", methods=['GET', 'POST'])
@login_required
def admin_add():
    if request.method == "POST":
        print(1)
        to_check = [('name-event', str), ('description-event', str), ('date-event', str), ('time-event', str),
                    ('location-event', str), ('price-event', float), ('seats-event', int)]
        if validate_greedy(to_check, request.form):
            print(2)
            LibraryDB().addEvent(request.form['name-event'], request.form['description-event'],
                                 request.form['date-event'], request.form['time-event'], request.form['location-event'],
                                 request.form['seats-event'], request.form['price-event'], None, '', current_user.user[1])
            #------------- заполнить по поступлению
        else:
            pass
            # flash("Не все поля заполнены")
    return render_template("admin/add.html")


@app.route("/admin/login", methods=['GET', 'POST'])
def admin_login():
    if request.method == "POST":
        to_check = [('login', str), ('password', str)]
        if validate_greedy(to_check, request.form):
            user_in_db = LibraryDB().getUserByLogin(request.form['login'])
            if not user_in_db:
                pass
                # flash("Такого пользователя нет")
                # print("none")
            elif not check_password_hash(user_in_db[2], request.form['password']):
                pass
                # flash("Неверный пароль")
                # print(user_in_db[2], request.form['password'])
            else:
                user_to_login = User(db_user=user_in_db)
                remember = 'device' in request.form.keys()
                login_user(user_to_login, remember=remember)
                return redirect("/admin")
        else:
            pass
            # flash("Не все поля заполнены")
    return render_template("login.html")


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
def index():
    return render_template("index.html")

@app.route("/<path:filepath>.html")
@login_required
def html_router(filepath):
    template_name = f"admin/{filepath}.html"
    return render_template(template_name)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
