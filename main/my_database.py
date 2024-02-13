import sqlite3
from sqlite3 import Error


def delete_query(table, column, value):
    '''Создаёт запрос на удаление'''
    return f'DELETE FROM {table} WHERE {column} = {value}'


def add_query(table, column, value):
    '''Создаёт запрос на вставку'''
    return f'INSERT INTO {table} {column} VALUES {value};'


def create_connection(path):
    '''создаёт связь с базой данных'''
    connection = None
    try:
        connection = sqlite3.connect(path, check_same_thread=False)
        print('Соединение с базой данных прошло успешно!')
    except Error as e:
        print(f'Произошла ошибка {e}')
    return connection


connection = create_connection(r'D:\pythonProjects\PycharmProjects\your_salary_project\main\db_main.sqlite')


def execute_query(con, query):
    '''выполняет запросы'''
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        con.commit()
        print('Запрос выполнен успешно')
    except Error as e:
        print(f'Произошла ошибка {e}')


def execute_read_query(connection, query):
    '''читает данные из базы данных'''
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"The error '{e}' occurred")


create_salary_table = """
CREATE TABLE IF NOT EXISTS salary (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  date DATE,
  amount INTEGER
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

select = 'SELECT * from salary'
salarys = execute_read_query(connection, select)
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

    for salary in salarys:  # смотрим все данные из базы
        print(salary)
