import sqlite3
from sqlite3 import Error

from main.app import render_date


def get_date_and_salary(user, *args):
    # Печатает дату и зарплату для конкретного пользователя
    data = execute_read_query(connection, f'SELECT {",".join(args)} FROM salary_users WHERE username = "{user}"')
    for date, salary in data:
        print(f'{render_date(date)}: {int(float(salary))} руб.')


def delete_query(table, column, value):
    '''Создаёт запрос на удаление'''
    return f'DELETE FROM {table} WHERE {column} = {value}'


def select_query(table, column, column1, value):
    '''Создаёт запрос на удаление'''
    return f'SELECT {column} FROM {table} WHERE {column1} = {value}'


def add_query(table, column, value):
    '''Создаёт запрос на вставку'''
    return f'INSERT INTO {table} {column} VALUES {value};'


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


create_salary_users_table = """
CREATE TABLE IF NOT EXISTS salary_users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT,
  date TEXT,
  amount TEXT
);
"""

create_salary = f"""
        INSERT INTO
          salary (date, amount)
        VALUES
          ('2024-02-13', '1000')
          ;
        """

# execute_query(connection, create_salary)

# select = 'SELECT * from users WHERE name = "dimapolenov" OR email = "dima@mail.ru"'
# users = execute_read_query(connection, select)
# select_post_description = "SELECT amount FROM salary WHERE id = 2"
# post_description = execute_read_query(connection, select_post_description)
add_column = 'ALTER TABLE salary_users ADD hours INT NOT NULL DEFAULT 0'
rename_column = 'ALTER TABLE salary_users RENAME COLUMN amount TO salary'
update_post_description = """
UPDATE
  salary
SET
  amount = 1000
WHERE
  id = 2
"""
# delete_date = f'DELETE FROM salary WHERE id = 2'
# execute_query(connection, delete_date)
if __name__ == '__main__':
    # print(execute_read_query(connection, 'SELECT date,amount FROM salary_users WHERE username = "misha"'))
    # get_date_and_salary('misha', 'date', 'amount')
    execute_query(connection, 'ALTER TABLE users RENAME COLUMN name TO username')