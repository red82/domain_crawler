from app import app, db, models
from datetime import datetime
from forms import LookupForm
from flask import render_template, redirect, request


@app.route('/')
@app.route('/index')
def index():
    form = LookupForm()

    return render_template('user_interface/lookup.html',
                           title='Lookup',
                           form=form)

@app.route('/get_data')
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
        raw_data = request.form['domain_list']
    else:
        redirect('/')

    data = splitter(raw_data)

    db_saver(data)

    return render_template('user_interface/get_data.html',
                           title='Get data',
                           data=data)