from json import loads
from classes import User


def load_users():
    users = []
    with open('init_data.json', 'r', encoding='utf8') as file:
        json_data = loads(file.read())
    for index, person in enumerate(json_data):
        user = User(index, person['first_name'], person['last_name'])
        users.append(user)
    return users


def process_int_input(message, quit_on_fail=False):
    value = input(message)
    try:
        value = int(value)
    except ValueError:
        print('Ошибка. Введено не числовое значение.')
        if quit_on_fail:
            print('Выходим из программы.')
            quit()
        return False
    return value

