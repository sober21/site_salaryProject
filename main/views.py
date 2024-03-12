import os
from datetime import date, datetime

from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash

from main.app import salary_of_one_day, render_date, convert_salary_and_date, \
    valid_register_data, get_hour_price, get_position_price
from main.my_database import execute_query, connection, execute_read_query, \
    get_first_day_week, get_salary_data_week, get_sum_of_week, get_salary_data_month, get_sum_of_month

app = Flask(__name__)

app.secret_key = os.urandom(23).hex()
current_date = date.today()
user_date = date.today()


@app.route("/", methods=["POST", "GET"])
def index():
    ref = 'Вход'
    if 'email' in session and 'password' in session:
        ref = 'Личный кабинет'
    return render_template('index.html', title='Главная страница', ref=ref)


@app.route('/dashboard', methods=['POST', 'GET'])
def dashboard():
    ref = 'Личный кабинет'
    cur_date = current_date
    global user_date
    workplace, *d = execute_read_query(connection,
                                       f'SELECT workplace, username, job_title from users WHERE email = "{session["email"]}"')[0]

    if request.method == 'POST':
        sal_today, sal_data, sum_of_period = None, None, None
        form = tuple(request.form.keys())[-1]

        action_week = '+' if 'next_week' in form else ('-' if 'last_week' in form else None)
        if form in ('get_week', 'next_week', 'last_week'):  # За неделю
            first_day_week = get_first_day_week(user_date)
            sal_data, cur = get_salary_data_week(email=session["email"], first_day=first_day_week)(action_week)
            if sal_data:
                sum_of_period = get_sum_of_week(email=session['email'], first_day=first_day_week)
                sal_data = convert_salary_and_date(sal_data, workplace=workplace)
                sum_of_period = convert_salary_and_date(sum_of_period(action_week), workplace=workplace, sums=True)
            user_date = cur

        action_month = '+' if 'next_month' in form else ('-' if 'last_month' in form else None)
        if form in ['get_month', 'next_month', 'last_month']:  # За месяц
            sal_data, cur = get_salary_data_month(email=session['email'], cur_data=user_date)(action_month)
            if sal_data:
                sum_of_period = get_sum_of_month(email=session['email'], cur_data=user_date)
                sal_data = convert_salary_and_date(sal_data, workplace=workplace)
                sum_of_period = convert_salary_and_date(sum_of_period(action_month), workplace=workplace, sums=True)
            user_date = cur

        elif 'date' in request.form and 'hours' in request.form and 'positions' in request.form:
            date = request.form.get('date')
            hours = request.form.get('hours')
            positions = request.form.get('positions')
            if not hours:
                hours = 0
            if 'mens' in request.form and 'incoming_positions' in request.form:
                mens = request.form.get('mens')
                incoming_positions = request.form['incoming_positions']
            else:
                mens, incoming_positions = 1, 0
            price = execute_read_query(connection,
                                       f'SELECT hour_price, position_price FROM price WHERE email = "{session["email"]}"')
            pr_hour, pr_pos = price[0][0], price[0][1]
            salary = salary_of_one_day(workplace=workplace, h=hours, pos=positions, emp=mens, inc_pos=incoming_positions,
                                       pr_hour=pr_hour, pr_pos=pr_pos, )

            if 'optional' in request.form:
                execute_query(connection,
                              f'INSERT INTO salary_users (email, date, salary, hours, positions, incoming_positions) '
                              f'VALUES("{session["email"]}", "{date}", {salary}, {hours}, '
                              f'{int(int(positions) / int(mens))}, {int(int(incoming_positions) / int(mens))}) '
                              f'ON CONFLICT(email, date) DO UPDATE '
                              f'SET salary=salary+{salary}, hours=hours+{hours}, '
                              f'positions=positions+{int(int(positions) / int(mens))}, '
                              f'incoming_positions=incoming_positions+{int(int(incoming_positions) / int(mens))}')

            else:
                execute_query(connection,
                              f'REPLACE INTO salary_users (email, date, salary, hours, positions, incoming_positions) '
                              f'VALUES("{session["email"]}", "{date}", {salary}, {hours}, '
                              f'{int(int(positions) / int(mens))}, {int(int(incoming_positions) / int(mens))})')
            date = render_date(date)
            sal_today = f'{date}: {int(salary)} руб.'
        return render_template('dashboard.html', workplace=workplace, cur_date=cur_date, sal_data=sal_data,
                               sal_today=sal_today,
                               sum=sum_of_period, email=session['email'], us=user_date, form=form, d=d, ref=ref)
    return render_template('dashboard.html', workplace=workplace, cur_date=cur_date, title='Добавить',
                           email=session['email'], us=user_date, d=d, ref=ref)


@app.route('/login', methods=['POST', 'GET'])
@app.route('/login')
def login():
    ref = 'Вход'
    msg = ''
    if 'email' in session and 'password' in session:
        return redirect(url_for('dashboard'))
    elif request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        account = execute_read_query(connection,
                                     f'SELECT password FROM users WHERE email = "{email}"')
        if account:
            if check_password_hash(account[0][0], password):
                session['email'] = email
                session['password'] = password
                return redirect(url_for('dashboard'))
            else:
                msg = 'Неправильное имя или пароль'
        else:
            msg = 'Неправильное имя или пароль'

    return render_template('login.html', title='Личный кабинет', msg=msg, ref=ref)


@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('password', None)
    return redirect(url_for('login'))


@app.route('/register', methods=['POST', 'GET'])
def register():
    ref = 'Вход'
    msg = ''
    if request.method == 'POST' and all(
            [request.form['email'], request.form['password'], request.form['replay_password'],
             request.form['username'], request.form['job_title'], request.form['workplace']]):
        password = request.form['password']
        replay_password = request.form['replay_password']
        email = request.form['email']
        username = request.form['username']
        job_title = request.form['job_title']
        workplace = request.form['workplace']
        if password == replay_password:
            account = execute_read_query(connection,
                                         f'SELECT * FROM users WHERE email = "{email}"')
            if not account:
                if valid_register_data(email=email, password=password):
                    hour_price = get_hour_price(job_title=job_title)
                    position_price = get_position_price(workplace=workplace)
                    session['email'] = email
                    session['password'] = password
                    password = generate_password_hash(password)
                    execute_query(connection, f'insert into users (email, password, username, job_title, workplace) '
                                              f'values("{email}", "{password}", "{username}", "{job_title}", "{workplace}")')
                    execute_query(connection, f'INSERT INTO price (email, hour_price, position_price) '
                                              f'values ("{session["email"]}", {hour_price}, {position_price})')
                    return redirect(url_for('dashboard'))
                else:
                    msg = 'Пароль должен быть не менее 8 символов, латинские буквы, цифры, знаки, без пробелов'
            else:
                msg = 'Пользователь с такой электронной почтой уже существует'
        else:
            msg = 'Пароли не совпадают'
    return render_template('register.html', msg=msg, ref=ref)


if __name__ == '__main__':
    pass
