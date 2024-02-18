import sqlite3
from sqlite3 import Error
from main.main import render_date


def delete_query(table, column, value):
    '''Создаёт запрос на удаление'''
    return f'DELETE FROM {table} WHERE {column} = {value}'


def select_query(table, column, column1, value):
    '''Создаёт запрос на удаление'''
    return f'SELECT {column} FROM {table} WHERE {column1} = {value}'


def add_query(table, column, value):
    '''Создаёт запрос на вставку'''
    return f'INSERT INTO {table} {column} VALUES {value};'


def create_connection(path):
    '''Создаёт связь с базой данных'''
    connection = None
    try:
        connection = sqlite3.connect(path, check_same_thread=False)
        print('Соединение с базой данных прошло успешно!')
    except Error as e:
        print(f'Произошла ошибка {e}')
    return connection


with open('db_path') as path:
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


create_user_salary_table = """
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

select = 'SELECT * from users WHERE name = "dimapolenov" OR email = "dima@mail.ru"'
users = execute_read_query(connection, select)
# select_post_description = "SELECT amount FROM salary WHERE id = 2"
# post_description = execute_read_query(connection, select_post_description)

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
    misha = execute_read_query(connection, 'SELECT * FROM salary_users WHERE username = "misha"')
    for i in misha:
        print(render_date(i[2]))
