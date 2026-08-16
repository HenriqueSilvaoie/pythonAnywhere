#from datetime import datetime
from flask import Flask, render_template, request, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Abidi@1329'


bootstrap = Bootstrap(app)
moment = Moment(app)

class NameForm(FlaskForm):
    name = StringField('What is your name?', validators= [DataRequired()])
    submit = SubmitField('Submit')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash('Looks like you have changed your name!')
        session['name'] = form.name.data
        return redirect(url_for('index'))
    return render_template('index.html',form=form, name = session.get('name'))


@app.route('/user/<name>/<pront>/<inst>')
def user(name, pront, inst):
    return render_template('user.html', name=name, pront=pront, inst=inst)


@app.route('/contextorequisicao/<name>')
def contexto(name):
    return render_template(
        'contexto.html',
        name=name,
        user_agent=request.headers.get('User-Agent'),
        ip=request.remote_addr,
        host=request.host
    )

