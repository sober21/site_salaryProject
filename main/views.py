import os

from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash

from main.app import current_data, salary_of_one_day, render_date, get_email, get_username, convert_salary_and_date, \
    valid_register_data
from main.my_database import execute_query, connection, add_query, execute_read_query, \
    first_day_week

app = Flask(__name__)

current_data = current_data
app.secret_key = os.urandom(23).hex()


@app.route("/", methods=["POST", "GET"])
def index():
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
                               title='Главная страница', date=date, res=res)
    return render_template('index.html', cur_date=current_data, title='Главная страница')


@app.route('/dashboard', methods=['POST', 'GET'])
def dashboard():
    anketa = execute_read_query(connection, f'SELECT username FROM employees WHERE username = "{session["username"]}"')
    if not anketa:
        return render_template('data_employees.html', ses=session['username'])
    if request.method == 'POST':
        try:
            if all([request.form['name'], request.form['hour_price'], request.form['position_price'],
                    request.form['job_title'], request.form['workplace']]):
                name, hour_price, position_price, job_title, workplace = request.form['name'], request.form[
                    'hour_price'], \
                    request.form['position_price'], request.form['job_title'], request.form['workplace']
                execute_query(connection,
                              f'insert into employees (username, name, job_title, workplace, hour_price, position_price) '
                              f'values ("{session["username"]}", "{name}", "{job_title}", "{workplace}", {hour_price}, {position_price})')

                return redirect(url_for('dashboard'))
        except KeyError:
            pass
        print(session['username'])
        sal_today, sal_data, sum_of_period = None, None, None
        if 'get_salary' in request.form:
            sal_data = execute_read_query(connection,
                                          f'SELECT date,hours,salary FROM salary_users WHERE '
                                          f'username = "{session["username"]}" ORDER BY date ASC')
            sum_of_period = execute_read_query(connection, f'SELECT SUM(salary), SUM(hours) FROM salary_users WHERE '
                                                           f'username = "{session["username"]}"')
            sal_data = convert_salary_and_date(sal_data)
        elif 'get_week' in request.form:
            first_day = first_day_week(current_data)
            sal_data = execute_read_query(connection, f'SELECT date, hours, salary FROM salary_users WHERE '
                                                      f'username = "{session["username"]}" and date >= "{first_day}" '
                                                      f'ORDER BY date ASC')
            sum_of_period = execute_read_query(connection, f'SELECT SUM(salary), SUM(hours) FROM salary_users WHERE '
                                                           f'username = "{session["username"]}" and date >= "{first_day}"')

            sal_data = convert_salary_and_date(sal_data)
        elif 'get_month' in request.form:
            sal_data = execute_read_query(connection, f'SELECT date, hours, salary FROM salary_users '
                                                      f'WHERE username = "{session["username"]}" and '
                                                      f'strftime("%m", date) >= strftime("%m", "now") '
                                                      f'ORDER BY date ASC')
            sum_of_period = execute_read_query(connection, f'SELECT SUM(salary),SUM(hours) FROM salary_users '
                                                           f'WHERE username = "{session["username"]}" and '
                                                           f'strftime("%m", date) >= strftime("%m", "now")')
            sal_data = convert_salary_and_date(sal_data)
        elif 'date' in request.form and 'hours' in request.form and 'positions' in request.form and 'mens' in request.form:
            date = request.form.get('date')
            hours = request.form.get('hours')
            positions = request.form.get('positions')
            mens = request.form.get('mens')
            salary = salary_of_one_day(hours, positions, mens)
            create_user_salary = add_query('salary_users', ('username', 'date', 'salary', 'hours'),
                                           (session['username'], date, salary, hours))
            execute_query(connection, create_user_salary)
            date = render_date(date)
            sal_today = f'{date}: {int(salary)} руб.'
        return render_template('dashboard.html', cur_date=current_data, sal_data=sal_data, sal_today=sal_today,
                               sum=sum_of_period, username=session['username'])
    return render_template('dashboard.html', cur_date=current_data, title='Добавить', username=session['username'])


@app.route('/login/', methods=['POST', 'GET'])
@app.route('/login/')
def login():
    msg = ''
    if 'username' in session and 'password' in session:
        return redirect(url_for('dashboard'))
    elif request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        account = execute_read_query(connection,
                                     f'SELECT password FROM users WHERE username = "{username}"')
        if check_password_hash(account[0][0], password):
            session['username'] = username
            session['password'] = password
            return redirect(url_for('dashboard'))
        else:
            msg = 'Неправильное имя или пароль'
    return render_template('login.html', title='Личный кабинет', msg=msg)


@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('password', None)
    return redirect(url_for('login'))


@app.route('/register', methods=['POST', 'GET'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        account = execute_read_query(connection,
                                     f'SELECT * FROM users WHERE username = "{username}" OR email = "{email}"')
        if not account:
            if valid_register_data(username, password, email):
                session['username'] = username
                session['password'] = password
                password = generate_password_hash(password)
                execute_query(connection,
                              add_query(table='users', column=('username', 'password', 'email'),
                                        value=(username, password, email)))
                return redirect(url_for('dashboard'))
            else:
                msg = 'Имя пользователя должно быть не менее 4 символов. Только латинские буквы, цифры, нижнее подчёркивание.\n Пароль не менее 8 символов'
        else:
            existing_email = get_email(account)
            existing_username = get_username(account)
            if username in existing_username:
                msg = 'Пользователь с таким именем уже существует'
            elif email in existing_email:
                msg = 'Пользователь с такой электронной почтой уже существует'
    return render_template('register.html', msg=msg)


if __name__ == '__main__':
    pass
