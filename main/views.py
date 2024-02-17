from flask import Flask, render_template, request, redirect, url_for, session
from main.main import current_data, salary_of_one_day, render_date
from main.my_database import execute_query, connection, delete_query, add_query, select_query, execute_read_query
import os

app = Flask(__name__)

current_data = current_data
app.secret_key = os.urandom(23).hex()


@app.route("/", methods=["POST", "GET"])
def index():
    if 'username' in session:
        return redirect(url_for('users', name=session['username']))
    if request.method == 'POST':
        date = request.form.get('date')
        hours = request.form.get('hours')
        positions = request.form.get('positions')
        mens = request.form.get('mens')
        salary = salary_of_one_day(hours, positions, mens)
        date = render_date(date)
        res = int(salary)
        return render_template(r'index.html', cur_date=current_data,
                               title='Главная страница', date=date, res=res)
    return render_template(r'index.html', cur_date=current_data, title='Главная страница')


@app.route('/users/<name>')
@app.route('/users/')
def users(name=None):
    if name:
        return render_template('users.html', name=name, title='Личный кабинет')
    return redirect(url_for('login'))


@app.route('/login/', methods=['POST', 'GET '])
@app.route('/login/')
def login():
    msg = ''
    if request.method == 'POST':
        name = request.form['username']
        password = request.form['password']
        account = execute_read_query(connection, f'SELECT * FROM users WHERE name = {repr(name)} AND password = {repr(password)}')
        if account:
            return redirect(url_for('users', name=name))
        else:
            msg = 'Неправильное имя или пароль'
    return render_template('login.html', title='Личный кабинет', msg=msg)


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        if request.form['username'].isalnum():
            session['username'] = request.form['username']

        session['password'] = request.form['password']

        session['email'] = request.form['email']
        execute_query(connection,
                      add_query(table='users', column=('name', 'password', 'email'),
                                value=(session['username'], session['password'],
                                       session['email']
                                       )))
        return redirect(url_for('users', name=session['username']))
    return render_template('register.html')


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


if __name__ == '__main__':
    pass
