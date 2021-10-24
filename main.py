from flask import Flask, render_template, url_for
from flask import request
from logic import load_users
from classes import User, Office

app = Flask(__name__)


@app.route("/")
def index():
    if len(offices) == 0:
        return init()
    return render_template('main.html', page_title="Главная страница",
                           offices=offices, office_count=len(offices), waiting=queue)


@app.route("/init", methods=["POST", "GET"])
def init():
    if request.method == "POST":
        try:
            offices_count = int(request.form["offices_count"])
            global offices
            offices = [Office() for i in range(offices_count)]
            return index()
        except ValueError:
            return render_template('init.html', page_title="Повторная инициализация",
                                   error_message="Ошибка ввода количества офисов, повторите попытку.")
    return render_template('init.html', page_title="Инициализация")


users = load_users()
queue = []
offices = []

if __name__ == '__main__':
    app.run(debug=True)