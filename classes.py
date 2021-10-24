# Классы, описывающие офис и клиентов офиса

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