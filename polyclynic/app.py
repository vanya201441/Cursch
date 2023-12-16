# стандартные пакеты (которые не нужно скачивать извне)
import json

# стандартные пакеты (которые нужно дополнительно устанавливать)

from flask import Flask, render_template, session, redirect,url_for

# модули проекта (которые пишем сами)
from blueprints.entry.routes import entry_app
from blueprints.profile.routes import profile_app
from blueprints.authorization.routes import auth_app
from blueprints.reports.routes import report_app
from sql_provider import SQLProvider
from database import get_db_config

app = Flask(__name__)
db_config = json.load(open('configs/config.json'))

app.register_blueprint(profile_app, url_prefix='/profile')
app.register_blueprint(auth_app, url_prefix='/authorization')
app.register_blueprint(entry_app, url_prefix='/entry')
app.register_blueprint(report_app, url_prefix='/reports')

provider = SQLProvider('blueprints/profile/sql/')
app.config['SECRET_KEY'] = 'super secret key'
app.config['DB_CONFIG'] = get_db_config()


@app.route('/')
def index():
    if 'login' in session:
        return render_template('menu.html', log=1)
    else:
        return render_template('menu.html', log=0)


@app.route('/counter')  # ? Счётчик посещений сайта.
def count_visits():
    counter = session.get('count', None)
    if counter is None:
        session['count'] = 0
    else:
        session['count'] = session['count'] + 1
    return f"Your count: {session['count']}"


@app.route('/session-clear')  # ? Очистка сессии.
def clear_session():
    session.clear()
    return ''


@app.route('/exit')
def exit_handler():
    session.clear()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=7004)
