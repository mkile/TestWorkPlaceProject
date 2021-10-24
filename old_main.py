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










print(users)
# Main cycle
work_hour = 0

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
