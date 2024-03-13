import calendar
from datetime import datetime, date, timedelta
import sqlite3
from sqlite3 import Error

from werkzeug.security import generate_password_hash, check_password_hash

from main.app import render_date, convert_salary_and_date


def get_first_day_week(cur_date: datetime) -> datetime:
    # Возвращает первый день недели
    while True:
        if cur_date.isoweekday() == 1:
            return cur_date
        cur_date = cur_date - timedelta(days=1)


def get_date_and_salary(user, *args):
    # Печатает дату и зарплату для конкретного пользователя
    data = execute_read_query(connection, f'SELECT {",".join(args)} FROM salary_users WHERE username = "{user}"')
    for a_date, salary in data:
        print(f'{render_date(a_date)}: {int(float(salary))} руб.')


def create_connection(db_dir):
    '''Создаёт связь с базой данных'''
    connection = None
    try:
        connection = sqlite3.connect(db_dir, check_same_thread=False)
        print('Соединение с базой данных прошло успешно!')
    except Error as e:
        print(f'Произошла ошибка {e}')
    return connection


with open('db_path.txt') as path:
    path = path.read()
connection = create_connection(fr'{path}')


def execute_query(con, query):
    '''Выполняет запросы'''
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        con.commit()
        print('Запрос выполнен успешно')
    except Error as e:
        print(f'Произошла ошибка {e}')


def execute_read_query(connection, query):
    '''Читает данные из базы данных'''
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"The error '{e}' occurred")


def get_salary_data_week(email: str, first_day: datetime, connect=connection):
    def action(act=None):
        nonlocal first_day

        if act == '+':
            first_day = first_day + timedelta(weeks=1)
        elif act == '-':
            first_day = first_day - timedelta(weeks=1)
        last_day = first_day + timedelta(weeks=1)

        def wrapper():
            result = execute_read_query(connect, f'SELECT date, hours, salary, positions, incoming_positions '
                                                 f'FROM salary_users WHERE email = "{email}" and "{last_day}" > date and date >= "{first_day}" '
                                                 f'ORDER BY date ASC')
            return result, first_day

        return wrapper()

    return action


def get_sum_of_week(email: str, first_day, connect=connection):
    def action(act=None):
        nonlocal first_day
        if act == '+':
            first_day = first_day + timedelta(weeks=1)
        elif act == '-':
            first_day = first_day - timedelta(weeks=1)
        last_day = first_day + timedelta(weeks=1)

        def wrapper():
            result = execute_read_query(connect,
                                        f'SELECT SUM(salary), SUM(hours), SUM(positions), SUM(incoming_positions) '
                                        f'FROM salary_users WHERE email= "{email}" and "{last_day}" > date and date >= "{first_day}"')
            return result

        return wrapper()

    return action


def get_sum_of_month(email: str, cur_data: datetime, connect=connection):
    def action(act=None):
        nonlocal cur_data
        if act == '+':
            cur_data = cur_data + timedelta(days=calendar.monthrange(year=cur_data.year, month=cur_data.month)[1])
        elif act == '-':
            cur_data = cur_data - timedelta(days=calendar.monthrange(year=cur_data.year, month=cur_data.month)[1])

        def wrapper():
            result = execute_read_query(connect,
                                        f'SELECT SUM(salary),SUM(hours), SUM(positions), SUM(incoming_positions) '
                                        f'FROM salary_users WHERE email = "{email}" '
                                        f'and strftime("%Y%m", date) == strftime("%Y%m", "{cur_data}")')
            return result

        return wrapper()

    return action


def get_salary_data_month(email: str, cur_data: date, connect=connection):
    def action(act=None):
        nonlocal cur_data
        if act == '+':
            cur_data = cur_data + timedelta(days=calendar.monthrange(year=cur_data.year, month=cur_data.month)[1])
        elif act == '-':
            cur_data = cur_data - timedelta(days=calendar.monthrange(year=cur_data.year, month=cur_data.month)[1])

        def wrapper():
            result = execute_read_query(connect,
                                        f'SELECT date, hours, salary, positions, incoming_positions FROM salary_users '
                                        f'WHERE email = "{email}" and '
                                        f'strftime("%Y%m", date) == strftime("%Y%m", "{cur_data}")'
                                        f'ORDER BY date ASC')
            return result, cur_data

        return wrapper()

    return action


# create_salary_users_table = """
# CREATE TABLE IF NOT EXISTS salary_users (
#   id INTEGER PRIMARY KEY AUTOINCREMENT,
#   email TEXT,
#   date TEXT UNIQUE,
#   salary INTEGER,
#   hours INTEGER,
#   positions INTEGER
# );
# """

# create_salary = f"""
#         INSERT INTO
#           salary (date, amount)
#         VALUES
#           ('2024-02-13', '1000')
#           ;
#         """
# Удаление таблицы
# execute_query(connection, 'DROP TABLE salary_users')

# Удаление всех данных из таблицы
# execute_query(connection, 'DELETE FROM salary_users')

# Удаление 1 записи из таблицы
# execute_query((connection, 'DELETE FROM salary_users WHERE id = 2'))

# Все таблицы в базе
table = execute_read_query(connection, 'SELECT * FROM sqlite_master where type="table"')  # все таблицы
# for i in table:
#     print(i)

# Все данные в таблице
# salary_users = execute_read_query(connection, 'SELECT * FROM salary_users')
# for i in salary_users:
#     print(i)

# Работа с датой
# SELECT * FROM table WHERE date_column BETWEEN '2021-01-01' and '2021-12-31' #выбрать данные между двумя датами
# SELECT * FROM table WHERE DATE(date_column) = DATE('now','-1 day');  #выбрать данные созданные вчера
# SELECT * FROM table WHERE time_column > '12:00:00';  #выбрать данные созданные после определённой даты
# SELECT * FROM table WHERE strftime('%m',date_column) = '04';  #выбрать данные в определённом месяце
# SELECT * FROM table_name ORDER BY datetime_column DESC;  #сортировка в порядке убывания


# add_column = 'ALTER TABLE salary_users ADD order_name TEXT DEFAULT "---"'
# rename_column = 'ALTER TABLE salary_users RENAME COLUMN amount TO salary'
# update_post_description = """
# UPDATE
#   salary
# SET
#   amount = 1000
# WHERE
#   id = 2
# """
# delete_date = f'DELETE FROM salary WHERE id = 2'
# execute_query(connection, delete_date)
if __name__ == '__main__':
    # execute_query(connection, 'DROP TABLE users')
    # execute_query(connection,
    #               'CREATE TABLE IF NOT EXISTS price (email TEXT NOT NULL UNIQUE, '
    #               'hour_price INTEGER NOT NULL, position_price INTEGER NOT NULL)')
    # execute_query(connection, 'DROP TABLE salary_users')
    # execute_query(connection, 'CREATE TABLE salary_users (email TEXT, '
    #                           'date TEXT, salary INTEGER NOT NULL, hours INTEGER NOT NULL, '
    #                           'positions INTEGER DEFAULT 0, incoming_positions INTEGER DEFAULT 0, UNIQUE(email, date))')

    # print(u)
    # execute_query(connection, 'ALTER TABLE salary_users ADD incoming_positions INTEGER DEFAULT 0')
    # us = execute_read_query(connection, 'select email from users')
    # print(us)
    # sal_data = execute_read_query(connection,
    #                               f'SELECT date,hours,salary, positions, incoming_positions FROM salary_users WHERE '
    #                               f'email = "dima@mail.ru" ORDER BY date ASC')
    # for i in us:
    #     print(i)

    pass
