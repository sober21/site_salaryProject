from flask import Flask, render_template, request, redirect, url_for, session
from main.main import current_data, salary_of_one_day, render_date, get_email, get_username
from main.my_database import execute_query, connection, delete_query, add_query, select_query, execute_read_query
import os

app = Flask(__name__)

current_data = current_data
app.secret_key = os.urandom(23).hex()


@app.route("/", methods=["POST", "GET"])
def index():
    ses = session.items()
    if 'username' in session and 'password' in session:
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        date = request.form.get('date')
        hours = request.form.get('hours')
        positions = request.form.get('positions')
        mens = request.form.get('mens')
        salary = salary_of_one_day(hours, positions, mens)
        date = render_date(date)
        res = int(salary)
        return render_template('index.html', cur_date=current_data,
                               title='Главная страница', date=date, res=res, sess=ses)
    return render_template('index.html', cur_date=current_data, title='Главная страница', sess=ses)


@app.route('/dashboard', methods=['POST', 'GET'])
def dashboard():
    ses = session.items()
    if request.method == 'POST':
        date = request.form.get('date')
        hours = request.form.get('hours')
        positions = request.form.get('positions')
        mens = request.form.get('mens')
        salary = salary_of_one_day(hours, positions, mens)
        create_user_salary = add_query('salary_users', ('username', 'date', 'amount'),
                                       (session['username'], date, salary))
        execute_query(connection, create_user_salary)
        date = render_date(date)
        res = f'{date}: {int(salary)} руб.'
        return render_template('dashboard.html', cur_date=current_data, res=res, username=session['username'], sess=ses)
    return render_template('dashboard.html', cur_date=current_data, title='Добавить', username=session['username'], sess=ses)


@app.route('/users/<name>')
@app.route('/users/')
def users(name=None):
    if name:
        return render_template('users.html', name=name, title='Личный кабинет')
    return redirect(url_for('index'))


@app.route('/login/', methods=['POST', 'GET'])
@app.route('/login/')
def login():
    ses = session.items()
    msg = ''
    if 'username' in session and 'password' in session:
        return redirect(url_for('dashboard', sess=ses))
    elif request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        account = execute_read_query(connection,
                                     f'SELECT * FROM users WHERE name = "{username}" AND password = "{password}"')
        if account:
            session['username'] = username
            session['password'] = password
            return redirect(url_for('dashboard', sess=ses))
        else:
            msg = 'Неправильное имя или пароль'
    return render_template('login.html', title='Личный кабинет', msg=msg, sess=ses)


@app.route('/register', methods=['POST', 'GET'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        account = execute_read_query(connection,
                                     f'SELECT * FROM users WHERE name = "{username}" OR email = "{email}"')
        if not account:
            session['username'] = username
            session['password'] = password
            execute_query(connection,
                          add_query(table='users', column=('name', 'password', 'email'),
                                    value=(username, password, email)))
            return redirect(url_for('dashboard'))
        else:
            existing_email = get_email(account)
            existing_username = get_username(account)
            if username in existing_username:
                msg = 'Пользователь с таким именем уже существует'
            elif email in existing_email:
                msg = 'Пользователь с такой электронной почтой уже существует'
    return render_template('register.html', msg=msg)


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
