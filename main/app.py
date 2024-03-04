from datetime import datetime, date
import locale
from string import ascii_lowercase, ascii_uppercase

locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')

PRICE_OF_HOUR = 91
PRICE_OF_POSITION = 3.7

current_date = datetime.today()


def get_username(acc):
    res = [i[1] for i in acc]
    return res


def get_hour_price(job_title: str) -> int:
    # Возращает стоимость часа в зависимости от должности
    result = 89
    if job_title == 'Кладовщик':
        result = 91
    elif job_title == 'Пом.кладовщика':
        result = 90
    return result


def get_position_price(workplace: str) -> int | float:
    # Возращает стоимость позиции в зависимости от должности
    result = 3.7
    if workplace == '3 отдел':
        result = 4.7
    elif workplace == 'Упаковка':
        result = 3
    return result


def valid_register_data(email, password):
    return all((is_valid_password(password), is_valid_email(email)))


def is_latins_letters(word: str) -> bool:
    # Проверяет, что все буквенные символы в слове - латинские
    chars = ascii_lowercase + ascii_uppercase
    for char in word:
        if char.isalpha():
            if char in chars:
                continue
            else:
                return False
    return True


def is_valid_username(username: str) -> bool:
    # Проверяет правильность имени пользователя(не менее 4 символов, обязательно 1 латинская буква(можно цифры,
    # нижнее подчёркивание), без пробелов)
    if len(username) >= 4 and not username.replace('_', '').isdigit() and username.replace('_', '').isalnum():
        if is_latins_letters(username):
            return True
    return False


def is_valid_password(password: str) -> bool:
    # Проверяет правильность пароля(не менее 8 символов, латинские буквы, цифры, знаки, без пробелов)
    if len(password) >= 8 and password.isprintable() and password.replace(' ', '') == password:
        if is_latins_letters(password):
            return True
    return False


def is_valid_email(email: str) -> bool:
    # Проверяет правильность электронной почты(латинские буквы, цифры, 1 символ "@", 1 символ ".", начинается не с "@" или
    # другого знака препинания, наличие букв между символами "@" и ".")
    if email.count('@') == 1 and email.count('.') == 1 and email.index('@') < email.index('.') and email.replace(' ',
                                                                                                                 '') == email:
        mail_domen = email.split('@')[1].split('.')[0]
        high_domen = email.split('.')[1]
        mail_name = email.split('@')[0]
        if mail_domen.isalnum() and not mail_domen.isdigit() and len(mail_domen) > 1 and mail_name.replace('_',
                                                                                                           '').isalnum() and \
                not mail_name.replace('_', '').isdigit() and high_domen.isalpha() and 4 > len(high_domen) > 1:
            if is_latins_letters(email):
                return True
    return False


def get_email(acc):
    res = [i[2] for i in acc]
    return res


def convert_salary_and_date(array, workplace, sums=False):
    # Поочерёдно возвращает форматированную дату, часы, позиции, приход и форматированную зарплату
    if array:
        if workplace[0][0] in ['1 отдел', '3 отдел']:
            if sums:
                for salary, hours, positions, incoming_positions in array:
                    yield hours, positions, incoming_positions, f'{int(float(salary))} руб'
            else:
                for dt, hours, salary, positions, incoming_positions in array:
                    yield render_date(dt), hours, positions, incoming_positions, f'{int(float(salary))} руб'
        elif workplace[0][0] == 'Упаковка':
            if sums:
                for salary, hours, positions, incoming_positions in array:
                    yield hours, positions, f'{int(float(salary))} руб'
            else:
                for dt, hours, salary, positions, incoming_positions in array:
                    yield render_date(dt), hours, positions, f'{int(float(salary))} руб'
    else:
        yield 0, 0, 0, 0


def change_month_name(month):
    if month[-1] == 'т':
        month = month + 'а'
    else:
        month = month[:-1] + 'я'
    return month


def render_date(dt: str) -> str:
    # Преобразует дату в нужный формат. Из '2022-02-12' получается '12 февраля'
    my_date = datetime.strptime(dt, '%Y-%m-%d')
    my_date = my_date.strftime('%d %B')
    day, month = my_date.split()[0], change_month_name(my_date.split()[-1])
    my_date = f'{int(day)} {month}'
    return my_date


def salary_of_one_day(h, pos, pr_hour, pr_pos, inc_pos=0, emp=1) -> int:
    # Считает зарплату за один день и возвращает число
    if emp == 1 and inc_pos == 0:
        salary = int(h) * int(pr_hour) + int(pos) * float(pr_pos)
    elif inc_pos != 0:
        salary = int(h) * int(pr_hour) + (int(pos) / int(emp)) * float(pr_pos) + (int(inc_pos) / int(emp)) * 7
    else:
        salary = int(h) * int(pr_hour) + (int(pos) / int(emp)) * float(pr_pos)
    return int(salary)


if __name__ == '__main__':
    # cur = datetime.today()
    # cur = datetime(day=cur.day, month=cur.month, year=cur.year)
    # last = datetime(year=2024, month=2, day=7)
    pass
