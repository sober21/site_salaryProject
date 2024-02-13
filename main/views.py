from flask import Flask, render_template, request
from main.main import current_data, salary_of_one_day, render_date
from main.my_database import execute_query, connection
app = Flask(__name__)

current_data = current_data


@app.route("/", methods=["POST", "GET"])
def hello_world():
    if request.method == "POST":
        language = request.form.get('language')
        framework = request.form['framework']
        return '<h1> The language is {}. The framework is {}.</h1>'.format(language, framework)
    return render_template(r'index.html', cur_date=current_data)


@app.route("/one/<name>")
@app.route("/one/")
def one_page(name=None):
    return render_template('one.html', name=name)


@app.route('/date', methods=['POST', 'GET'])
def get_date():
    if request.method == 'POST':
        date = request.form.get('date')
        hours = request.form.get('hours')
        positions = request.form.get('positions')
        mens = request.form.get('mens')
        salary = salary_of_one_day(hours, positions, mens)
        create_salary = f"INSERT INTO salary (date, amount) VALUES({repr(date)}, {salary});"
        execute_query(connection, create_salary)
        date = render_date(date)
        return f'{date}: {salary:.1f} руб.'
    return render_template('date.html', cur_date=current_data)


@app.route("/users/<username>")
def get_profile_username(username):
    return f"Имя пользователя: {username}"


if __name__ == '__main__':
    app.run(debug=True)
