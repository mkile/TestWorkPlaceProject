from flask import Flask, render_template, url_for, redirect, send_from_directory
from flask import request
from src.logic import set_offices_count, get_offices_count, get_queue, get_users_in_offices, get_users_info, \
    try_to_add_user_to_office
from src.init import initialize_database
from sqlite3 import connect
import os

app = Flask(__name__)
DB_NAME = "data/database.db"


@app.route("/")
def index():
    if get_offices_count(connection()) == 0:
        return redirect(url_for("init"))
    offices = get_users_in_offices(connection())
    queue = get_queue(connection())
    return render_template('main.html', page_title="Главная страница",
                           offices=offices, office_count=len(offices), waiting=queue)


@app.route("/init", methods=["POST", "GET"])
def init():
    if request.method == "POST":
        try:
            offices_count = int(request.form["offices_count"])
            if offices_count < 1 or offices_count > 10:
                raise ValueError
            set_offices_count(connection(), offices_count)
            return redirect(url_for("index"))
        except Exception:
            return render_template('init.html', page_title="Повторная инициализация",
                                   error_message="Ошибка ввода количества офисов, повторите попытку.")
    return render_template('init.html', page_title="Инициализация")


@app.route("/add_user", methods=["POST", "GET"])
def add_user():
    if get_offices_count(connection()) == 0:
        return redirect(url_for("init"))
    title = "Добавление пользователя в список работающих в офисе."
    users = get_users_info(connection())
    users = [user for user in users if user['Office'] is None and user['Queue'] is None]
    if request.method == "GET":
        return render_template("add_user.html", page_title=title,
                               persons=users)
    elif request.method == "POST":
        try:
            user_id = int(request.form["user_id"])
            work_hours = int(request.form["working_hours"])
            try_to_add_user_to_office(connection(), user_id, work_hours)
            return redirect(url_for('index'))
        except ValueError:
            return render_template("add_user.html", page_title=title, persons=users,
                                   error_message="Передан недействительный номер пользователя")
    return index()


@app.route("/user_info", methods=["POST", "GET"])
def user_info():
    if get_offices_count(connection()) == 0:
        return redirect(url_for("init"))
    title = "Вывод информации о пользователе"
    users = get_users_info(connection())
    if request.method == "GET":
        return render_template("user_info.html", page_title=title, users_list=users, selected_user=-1)
    if request.method == "POST":
        try:
            user_id = int(request.form['selected_user'])
            user_id = [ind for ind, x in enumerate(users) if x['user_id'] == user_id][0]
        except ValueError:
            return render_template("user_info.html", page_title=title, users_list=users, selected_user=-1,
                                   error_message="Введено некоректное значение идентификатора пользователя")
        return render_template("user_info.html", page_title=title, users_list=users, selected_user=user_id)


@app.route("/skip_time", methods=["POST"])
def skip_time():
    """Перемещение на указанное количество часов вперед"""
    pass


@app.route("/favicon.ico")
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route("/stylesheet.css")
def stylesheet():
    return send_from_directory(os.path.join(app.root_path, 'templates/css'),
                               'stylesheet.css', mimetype='text/css')


@app.errorhandler(404)
def page_not_found(e):
    return render_template("error_page.html", page_title="Возникла ошибка.", error_message=e)


@app.errorhandler(500)
def internal_server_error(e):
    return render_template("error_page.html", page_title="Возникла внутренняя ошибка сервера.", error_message=e)


# Временно разместим процедуру создания соединения тут. Постоянное соединение в разных потоках не работает
def connection():
    """Создание соединения """
    return connect(DB_NAME)


app.config.from_pyfile('config.py')

if not initialize_database(connection()):
    quit("An error was encountered during initialization.")
if __name__ == '__main__':
    app.run(debug=True)
