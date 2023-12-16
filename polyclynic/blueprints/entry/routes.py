
from database import select_dict
from datetime import datetime
from flask import Blueprint, render_template, session, request, current_app, redirect, url_for
from sql_provider import SQLProvider
from blueprints.authorization.access import login_required, auth_required
from database import work_with_db,insert_into_db
import json

entry_app = Blueprint('entry', __name__, template_folder='templates')
db_config = json.load(open('configs/config.json'))
provider = SQLProvider('blueprints/entry/sql/')
basket = {}

@entry_app.route('/', methods=['GET', 'POST'])
def choose():
    global basket
    if request.method == 'GET':
        sql = provider.get('all_items.sql')
        items = select_dict(db_config, sql)
        # basket = session.get('basket', {})
        print(items)
        return render_template('basket_show.html', item=items, basket=basket, basket_keys=basket.keys())
    else:
        doc_id = request.form.get('doc_id')
        # print(doc_id)
        sql = provider.get('add_item.sql', id=doc_id)
        # print(sql)
        item = select_dict(db_config, sql)[0]
        add_to_basket(basket, item)
        # print(basket)
    return redirect(url_for('entry.choose'))


@entry_app.route('/sec')
def menu():
    global basket
    basket = {}
    return redirect('/second')

@entry_app.route('/clear')
def clear_basket():
    # if 'basket' in session:
    #     session.pop('basket')
    global basket
    basket = {}
    return redirect(url_for('entry.choose'))

def add_to_basket(bask, item):
    bask[item['doc_id']] = {'specialization': item['specialization'], 'bith_year': item['bith_year'],
                                      'amount': 1}


@entry_app.route('/save_order', methods=['GET', 'POST'])
def save_order():
    global basket
    user_id = session['login']
    if basket:
        sql = provider.get('insert_order.sql', user_id=user_id, user_date=datetime.now().strftime("%Y-%m-%d"))
        insert_into_db(db_config, sql)
        sql = provider.get('select_order_id.sql', user_id=user_id)
        # print(insert_into_db(db_config, sql)[0])
        order_id = select_dict(db_config, sql)[0]['max_id']

    for key in basket.keys():
        item = basket[key]
        sql = provider.get('insert_order_list.sql', order_id=order_id, doc_id=key)
        insert_into_db(db_config, sql)
    basket = {}
    return render_template('done.html')
