from flask import Blueprint, render_template, session, request, flash

from blueprints.authorization.access import auth_required
from sql_provider import SQLProvider
from database import work_with_db
import json


auth_app = Blueprint('authorization', __name__, template_folder='templates', static_folder='static')
db_config = json.load(open('configs/config.json'))
provider = SQLProvider('blueprints/authorization/sql/')


@auth_app.route('/', methods=['GET', 'POST'])
def login_page():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        login = request.form.get('login', '')
        password = request.form.get('password', '')
        sql = provider.get('sql.sql', login=login, password=password)
        group_user = work_with_db(db_config, sql)

        if not group_user:
            flash('relogin', 'error')
            return render_template('login.html')
        else:
            user_info = [group_user[0]['group_user'], group_user[0]['id_user']]
            session['group_name'] = user_info[0]
            session['login'] = user_info[1]
            return render_template('confirm.html', str='Вы успешно авторизовались!', group_user=user_info[0])
