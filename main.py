from flask import Flask, render_template, request, redirect, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required, current_user, logout_user
from user_class import User
from events import LibraryDB
from api_post import api_post
from api_get import api_get

www_path = 'www'
app = Flask(__name__, static_folder=www_path, static_url_path="", template_folder=www_path)
app.config["SECRET_KEY"] = "o8pjag5ny;o32g42vonny8libtfukjyj,gyukfyfkufyulgyuk"
login_manager = LoginManager(app)
login_manager.init_app(app)
# login_manager.login_view = 'login'

app.register_blueprint(api_get)
app.register_blueprint(api_post)
@login_manager.user_loader
def load_user(user_id):
    return User(user_id, LibraryDB())


@app.route("/admin", methods=['GET', 'POST'])
@login_required
def admin():
    if request.method == "POST":
        print(request.form.keys())
        if not False in [i in request.form.keys() for i in ['name', 'date', 'time', 'place']]:
            LibraryDB().addEvent(request.form['name'], None, request.form['date'], request.form['time'], request.form['place'], 0, 0, '', current_user[1])
        else:
            flash("Не все поля заполнены")
    return render_template("add-event.html")


@app.route("/admin/login", methods=['GET', 'POST'])
def alogin():
    if request.method == "POST":
        print(request.form.keys())
        if not False in [i in request.form.keys() and request.form[i] for i in ['login', 'password']]:
            user_in_db = LibraryDB().getUserByLogin(request.form['login'])
            print(user_in_db)
            if not user_in_db:
                flash("Такого пользователя нет")
            elif check_password_hash(user_in_db[2], request.form['password']):
                flash("Неверный пароль")
            else:
                user_to_login = User(db_user=user_in_db)
                remember = 'device' in request.form.keys() #тут будет работать не правильно, ключ 'device' имеет 3 состояния: None, False, True
                login_user(user_to_login, remember=remember)
                return redirect("/admin")
        else:
            flash("Не все поля заполнены")
    return render_template("login.html")


@app.route("/")
@app.route("/index")
def index():
    return redirect("/admin/login")


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
