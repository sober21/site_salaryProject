from datetime import datetime, date, timedelta
import locale
from string import ascii_lowercase, ascii_uppercase

locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')

PRICE_OF_HOUR = 91
PRICE_OF_POSITION = 3.7

current_data = date.today()


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


def convert_salary_and_date(array):
    # Поочерёдно возвращает форматированную дату, часы, позиции, приход и форматированную зарплату
    for dt, hours, salary, positions, incoming_positions in array:
        yield render_date(dt), hours, positions, incoming_positions, f'{int(float(salary))} руб'


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
    my_date = f'{day} {month}'
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


def get_last_date(file: str) -> datetime:
    '''Возаращает последнюю дату из файла'''
    with open(file, encoding='utf-8') as file_for_read:
        lst = file_for_read.readlines()
        year = ''
        for line in lst:
            if line.strip().endswith(' год'):
                year = line.strip().split()[0]
        last_writer = str(year) + ' ' + lst[-1].split(':')[0]  # берём из последней строки только дату
        last_date = datetime.strptime(last_writer, '%Y %d %B')
    return last_date


def empty_file(file: str) -> bool:
    '''проверяет - является ли файл пустым'''
    with open(file, encoding='utf-8') as f:
        try:
            next(f)
            return False
        except StopIteration:
            return True


def layaway_list(c_date: datetime, l_date: datetime) -> list:
    '''Возвращает список нерабочих дней, который надо будет записать в файл'''
    cur_date = c_date
    last_date = l_date + timedelta(days=1)
    res = []
    cur_month, cur_year = last_date.month, last_date.year
    while cur_date > last_date:
        if cur_year != last_date.year:
            cur_year = last_date.year
            res.append(f'{cur_year} год\n')
        if cur_month != last_date.month:
            cur_month = last_date.month
            res.append(f'{last_date.strftime("%B")}\n')

        res.append(f'{last_date.strftime("%d %B")}: выходной.\n')
        last_date += timedelta(days=1)

    return res


def valid_year(c, l):
    pass


def valid_month(c):
    pass


def write_in_file(sal) -> None:
    '''Записывет данные в файл'''
    file = 'for_text_files/salary1.txt'

    with open(file, 'a', encoding='utf-8') as file_for_write:
        cur_date = datetime.today()
        cur_date = datetime(year=cur_date.year, month=cur_date.month, day=cur_date.day)
        empty_f = empty_file(file)
        if empty_f:  # если файл пустой
            year = cur_date.year
            month = cur_date.strftime('%B')
            print(f'{year} год', file=file_for_write)
            print(f'{month}', file=file_for_write)
        else:
            last_date = get_last_date(file)

            if cur_date > last_date + timedelta(days=1):
                missed_days = layaway_list(cur_date, last_date)
                file_for_write.writelines(missed_days)
            else:
                if cur_date.year > last_date.year:
                    month = cur_date.strftime('%B')
                    print(f'{cur_date.year} год', file=file_for_write)
                    print(f'{month}', file=file_for_write)
                elif cur_date.month > last_date.month:
                    month = cur_date.strftime('%B')
                    print(f'{month}', file=file_for_write)
        cur_date = cur_date.strftime('%d %B')
        print(f'{cur_date}: {int(sal)} руб.', file=file_for_write)


def input_dates() -> tuple[int, int, int]:
    '''Получает и возваращает входные данные'''
    while True:
        try:
            hours = input('Часы:')
            positions = input('Количество позиций:')
            employee = input('Количество человек:')
            if hours == '':
                hours = '9'
            if positions == '':
                positions = '1'
            if employee == '':
                employee = '3'
            if not (hours + positions + employee).isdigit():
                raise TypeError
            break
        except TypeError:
            print('Введите число либо пустую строку.')
    hours, positions, employee = int(hours), int(positions), int(employee)
    return hours, positions, employee


def main():
    hours, positions, employee = input_dates()
    salary = salary_of_one_day(hours, positions, employee)
    write_in_file(salary)


if __name__ == '__main__':
    # cur = datetime.today()
    # cur = datetime(day=cur.day, month=cur.month, year=cur.year)
    # last = datetime(year=2024, month=2, day=7)
    pass
