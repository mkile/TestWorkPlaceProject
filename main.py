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
    first_name = ''
    last_name = ''
    start_work_time = 0
    end_work_time = 0
    work_time = 0
    remaining_work_time = 0
    working_now = False

    def __repr__(self):
        return f'First name: {self.first_name}, Last name: {self.last_name}, Worked hours {str(self.work_time)}, ' \
               f'Working now {self.working_now}'


class Office:
    def __init__(self):
        self.capacity = 12
        self.visitors = []

    def add_visitor(self, new_visitor):
        if len(self.visitors) < self.capacity:
            self.visitors.append(new_visitor)
            print(f'Пользователь {new_visitor} добавлен в офис')
        else:
            print('Свободных мест в офисе нет.')

    def checkout_visitors(self):
        checked_out_visitors = []
        remaining_visitors = []
        for index in range(len(self.visitors)):
            if self.visitors[index].remaining_work_time > 0:
                self.visitors[index].remaining_work_time -= 1
                self.visitors[index].work_time += 1
                if self.visitors[index].remaining_work_time == 0:
                    checked_out_visitors.append(self.visitors[index])
                else:
                    remaining_visitors.append(self.visitors[index])
        self.visitors = remaining_visitors
        return checked_out_visitors

    def get_free_places(self):
        return self.capacity - len(self.visitors)


users = []
with open('init_data.json', 'r', encoding='utf8') as file:
    json_data = loads(file.read())
for person in json_data:
    user = User()
    user.first_name = person['first_name']
    user.last_name = person['last_name']
    users.append(user)
print(users)
# Main cycle
work_hour = 0
offices = input('Введите количество офисов:')
try:
    offices = int(offices)
except ValueError as Err:
    print('Ошибка. Введено не числовое значение количества офисов.')
    quit()
while True:
    if work_hour >= 24:
        work_hour = 0
    input_result = False
    while not input_result:
        print('Час:', work_hour)
        print()
        result = input('Выберите вариант действий')
