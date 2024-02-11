from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def hello_world():
    return render_template(r'index.html')


@app.route("/one/<name>")
@app.route("/one/")
def one_page(name=None):
    return render_template('one.html', name=name)


@app.route("/second/")
def second_page():
    return "second_page with endpoint trailing slash"


@app.route("/second")
def second_page2():
    return render_template('second.html')


@app.route("/users/<username>")
def get_profile_username(username):
    return f"Имя пользователя: {username}"
