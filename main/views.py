import os
from datetime import date

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
    if 'email' in session and 'password' in session:
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        ind_date = request.form.get('date')
        hours = request.form.get('hours')
        positions = request.form.get('positions')
        mens = request.form.get('mens')
        salary = salary_of_one_day(h=hours, pos=positions, emp=mens, inc_pos=0)
        ind_date = render_date(ind_date)
        res = int(salary)
        return render_template('index.html',
                               title='Главная страница', date=ind_date, res=res)
    return render_template('index.html', title='Главная страница')


@app.route('/dashboard', methods=['POST', 'GET'])
def dashboard():
    cur_date = current_date
    global user_date
    action = None
    workplace = execute_read_query(connection, f'SELECT workplace from users WHERE email = "{session["email"]}"')
    if request.method == 'POST':
        sal_today, sal_data, sum_of_period = None, None, None
        if 'get_week' in request.form:  # За текущую неделю
            first_day_week = get_first_day_week(user_date)
            if get_salary_data_week(email=session["email"], first_day=first_day_week):
                sal_data = get_salary_data_week(email=session["email"], first_day=first_day_week)
                sum_of_period = get_sum_of_week(email=session['email'], first_day=first_day_week)
                sal_data = convert_salary_and_date(sal_data, workplace=workplace)
                sum_of_period = convert_salary_and_date(sum_of_period, workplace=workplace, sums=True)
        action = '+' if 'next_month' in request.form else ('-' if 'last_month' in request.form else None)
        if 'get_month' in request.form or 'next_month' in request.form or 'last_month' in request.form:  # За текущий месяц
            if get_salary_data_month(email=session['email'], cur_data=user_date)(action)[0]:
                sal_data, cur = get_salary_data_month(email=session['email'], cur_data=user_date)(action)
                sum_of_period = get_sum_of_month(email=session['email'], cur_data=user_date)
                sal_data = convert_salary_and_date(sal_data, workplace=workplace)
                sum_of_period = convert_salary_and_date(sum_of_period(action), workplace=workplace, sums=True)
                user_date = cur
        elif 'date' in request.form and 'hours' in request.form and 'positions' in request.form:
            date = request.form.get('date')
            hours = request.form.get('hours')
            positions = request.form.get('positions')
            if 'mens' in request.form and 'incoming_positions' in request.form:
                mens = request.form.get('mens')
                incoming_positions = request.form['incoming_positions']
            else:
                mens, incoming_positions = 1, 0
            price = execute_read_query(connection,
                                       f'SELECT hour_price, position_price FROM price WHERE email = "{session["email"]}"')
            pr_hour, pr_pos = price[0][0], price[0][1]
            salary = salary_of_one_day(h=hours, pos=positions, emp=mens, inc_pos=incoming_positions,
                                       pr_hour=pr_hour, pr_pos=pr_pos, )

            execute_query(connection,
                          f'REPLACE INTO salary_users (email, date, salary, hours, positions, incoming_positions) '
                          f'VALUES("{session["email"]}", "{date}", {salary}, {hours}, '
                          f'{int(int(positions) / int(mens))}, {int(int(incoming_positions) / int(mens))})')
            date = render_date(date)
            sal_today = f'{date}: {int(salary)} руб.'
        return render_template('dashboard.html', workplace=workplace, cur_date=cur_date, sal_data=sal_data,
                               sal_today=sal_today,
                               sum=sum_of_period, email=session['email'])
    return render_template('dashboard.html', workplace=workplace, cur_date=cur_date, title='Добавить',
                           email=session['email'])


@app.route('/login', methods=['POST', 'GET'])
@app.route('/login')
def login():
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

    return render_template('login.html', title='Личный кабинет', msg=msg)


@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('password', None)
    return redirect(url_for('login'))


@app.route('/register', methods=['POST', 'GET'])
def register():
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
                    msg = 'Пароль должен быть не менее 8 символов'
            else:
                msg = 'Пользователь с такой электронной почтой уже существует'
    return render_template('register.html', msg=msg)


if __name__ == '__main__':
    pass
