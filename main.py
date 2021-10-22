# Компания арендует офисы. В каждом офисе есть 12 мест. Сотрудников в компании значительно больше,
# но у них свободный график работы. Когда в офис приходит новый сотрудник он нажимает на кнопку "я пришел",
# и программа выдает ему место. Если в выбранном офисе нет мест - предлагает подождать и добавляет сотрудника
# в очередь, или же предлагает ему другой свободный офис. Когда сотрудник уходит он нажимает на кнопку "я ушел"
# и место освобождается. Начальник хочет иметь возможность проверять сколько времени сотрудники провели в офисе,
# а так же где есть конкретный сотрудник и есть ли он на работе.
#
# ⭐️ Задание со звездочкой - предусмотреть возможность размещения в офис не отдельного
# сотрудника, а целой команды по 3, 5 и 10 человек.
from json import loads


class User:
    def __init__(self, user_id, first_name, last_name):
        self.start_work_time = 0
        self.end_work_time = 0
        self.work_time = 0
        self.remaining_work_time = 0
        self.id = user_id
        self.first_name = first_name
        self.last_name = last_name

    def __repr__(self):
        return f'Имя: {self.first_name}, Фамилия: {self.last_name}, Отработано часов {str(self.work_time)}'


class Office:
    def __init__(self):
        self.capacity = 2
        self.visitors = []

    def add_visitor(self, new_visitor, user_work_hours):
        if len(self.visitors) < self.capacity:
            self.visitors.append(new_visitor)
            self.visitors[len(self.visitors) - 1].remaining_work_time = user_work_hours
            print(f'Сотрудник {new_visitor} добавлен в офис')
            return True
        else:
            return False

    def checkout_visitors(self):
        checked_out_visitors = []
        remaining_visitors = []
        for index in range(len(self.visitors)):
            if self.visitors[index].remaining_work_time > 0:
                self.visitors[index].remaining_work_time -= 1
                self.visitors[index].work_time += 1
                if self.visitors[index].remaining_work_time == 0:
                    checked_out_visitors.append(self.visitors[index].user_id)
                else:
                    remaining_visitors.append(self.visitors[index])
        self.visitors = remaining_visitors
        return checked_out_visitors

    # def get_free_places(self):
    #     return self.capacity - len(self.visitors)

    def check_user_presence(self, user_id):
        return sum([x.id for x in self.visitors if x.id == user_id]) > 0


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


users = []
queue = []
with open('init_data.json', 'r', encoding='utf8') as file:
    json_data = loads(file.read())
for index, person in enumerate(json_data):
    user = User(index, person['first_name'], person['last_name'])
    users.append(user)
print(users)
# Main cycle
work_hour = 0
offices = [Office() for i in range(process_int_input('Введите количество офисов:', True))]
while True:
    if work_hour >= 24:
        work_hour = 0
    input_result = False
    while not input_result:
        print('Текущий час:', work_hour)
        print(f'В {len(offices)} офисах работает {sum([len(x.visitors) for x in offices])}')
        print(f'В очереди находится {len(queue)} человек')
        print('1 - Добавить сотрудника желающего попасть в офис', '2 - Вывести статистику по конкретному сотруднику',
              '0 - Перейти к следующему часу', sep='\n')
        result = process_int_input('Выберите вариант действий:')
        if result == 1:
            user_index = process_int_input(f'Введите номер желающего попасть в офис от 0 до {len(users)}: ')
            if sum([off.check_user_presence(user_index) for off in offices]) > 0 or \
                    sum([x for x in queue if x == user_index]):
                print('Данный сотрудник уже работает в офисе.')
            else:
                if not(isinstance(user_index, bool)):
                    work_hours = process_int_input(f'Укажите количество часов которые сотрудник {users[user_index]} '
                                                   f'хочет проработать:')
                    if not (isinstance(work_hours, bool)):
                        not_found_place_for_new_visitor = True
                        for office_index in range(len(offices)):
                            if offices[office_index].add_visitor(users[user_index], work_hours):
                                users[user_index].working_now = True
                                not_found_place_for_new_visitor = False
                                break
                        if not_found_place_for_new_visitor:
                            users[user_index].remaining_work_time = work_hours
                            queue.append(users[user_index])
                            print(f'Сотруднику {users[user_index]} не хватило места в офисах, он поставлен в очередь')
        elif result == 2:
            user_index = process_int_input(f'Введите номер сотрудника от 0 до {len(users)}: ')
            if not (isinstance(user_index, bool)):
                print(users[user_index])
                in_office = sum([off.check_user_presence(user_index) for off in offices])
                if sum([off.check_user_presence(user_index) for off in offices]) > 0:
                if user_index in queue:
                    print(f'Сотрудник находится в очереди.')

        elif result == 0:
            input_result = True
        else:
            print('Неверный ввод !')
