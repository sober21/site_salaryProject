from flask import Flask, render_template, request
from main.main import current_data, salary_of_one_day, render_date
from main.my_database import execute_query, connection, delete_query, add_query, select_query, execute_read_query


app = Flask(__name__)

current_data = current_data


@app.route("/", methods=["POST", "GET"])
def hello_world():
    if request.method == 'POST':
        date = request.form.get('date')
        hours = request.form.get('hours')
        positions = request.form.get('positions')
        mens = request.form.get('mens')
        salary = salary_of_one_day(hours, positions, mens)
        date = render_date(date)
        res = int(salary)
        return render_template(r'index.html', cur_date=current_data, title='Главная страница', date=date, res=res)
    return render_template(r'index.html', cur_date=current_data, title='Главная страница')


app.route('/users/<name>')
def users(name=None):
    return render_template('users.html', name=name, title='Личный кабинет')


@app.route('/sign_in/')
def l_k():
    return render_template('sign_in.html', title='Личный кабинет')


@app.route('/date', methods=['POST', 'GET'])
def get_date():
    if request.method == 'POST':
        date = request.form.get('date')
        hours = request.form.get('hours')
        positions = request.form.get('positions')
        mens = request.form.get('mens')
        salary = salary_of_one_day(hours, positions, mens)
        create_salary = add_query('salary', ('date', 'amount'), (date, salary))
        execute_query(connection, create_salary)
        date = render_date(date)
        res = f'{date}: {int(salary)} руб.'
        return render_template('date.html', cur_date=current_data, res=res)
    return render_template('date.html', cur_date=current_data, title='Добавить')


@app.route('/date/select', methods=['POST', 'GET'])
def get_from_bd():
    if request.method == 'POST':
        date = request.form.get('date')
        query = select_query('salary', 'amount', 'date', date)
        lst = execute_read_query(connection, query)
        return render_template('select.html', cur_date=current_data, title='Выборка', context=lst)
    return render_template('select.html', cur_date=current_data, title='Выборка')

@app.route("/users/<username>")
def get_profile_username(username):
    return f"Имя пользователя: {username}"


if __name__ == '__main__':
    pass

