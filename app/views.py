from app import app, db, models
from datetime import datetime
from forms import LookupForm
from flask import render_template, redirect, request, jsonify, abort


class CustomException(Exception):
    pass


@app.route('/')
@app.route('/index')
def index():
    form = LookupForm()

    return render_template('user_interface/lookup.html',
                           title='Lookup',
                           form=form)

@app.route('/get_data', methods=['GET', 'POST'])
def get_data():

    def splitter(str):
        return str

    def db_saver(domain_list):
        req = models.Request(timestamp=datetime.utcnow(), domains=domain_list)
        db.session.add(req)
        db.session.commit()

    if request.method == 'GET':
        raw_data = request.args['domain_list']
    elif request.method == 'POST':
        data = request.files["file"]
        raw_data = data.read()
    else:
        redirect('/')

    data = splitter(raw_data)

    db_saver(data)

    form = LookupForm()

    return render_template('user_interface/lookup.html',
                           title='Enter another domains',
                           form=form)

    # return render_template('user_interface/get_data.html',
    #                        title='Get data',
    #                        data=data)

@app.route('/db')
def get_domains():
    domain = None
    try:
        domain = models.Request.query.order_by(models.Request.id.desc()).first()

    except CustomException:
        abort(404)

    if not domain:
        abort(404)

    return jsonify({'id': domain.id,
            'domains': domain.domains,
            'timestamp': domain.timestamp
    })