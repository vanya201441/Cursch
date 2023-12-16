# стандартные пакеты (которые не нужно скачивать извне)
import json

# стандартные пакеты (которые нужно дополнительно устанавливать)
from flask import session, request, render_template, flash, url_for, redirect
from functools import wraps


config = json.load(open('blueprints/authorization/configs/access.json'))

def auth_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if 'login' in session:
            return f(*args, **kwargs)
        else:
            return redirect(url_for('authorization.login_page'))
    return wrapper

def group_validation(config:dict, session: session) -> bool:
    group = session.get('group_name', 'unauthorized')
    book = {
        1: "",
        2: request.endpoint
    }
    target_app = book[len(request.endpoint.split('.'))]
    if group in config and target_app in config[group]:
        return True
    return False


def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if group_validation(config, session):
            return f(*args, **kwargs)
        else:
            flash('У вас нету доступа', 'error')
            return redirect(url_for('index'))
        # return render_template('confirm.html', str='У вас нет доступа.')
    return wrapper
