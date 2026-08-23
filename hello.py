#from datetime import datetime
from flask import Flask, render_template, request, session, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_moment import Moment, datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, PasswordField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Abidi@1329'

bootstrap = Bootstrap(app)
moment = Moment(app)

class NameForm(FlaskForm):
    name = StringField('Informe o seu nome: ', validators= [DataRequired()])
    sobrenome = StringField('Informe o seu sobrenome: ', validators= [DataRequired()])
    inst_ens = StringField('Informe a sua instituição de ensino: ', validators= [DataRequired()])
    disciplina = SelectField('Informe a disciplina: ', choices=[('DSWA5'), ('DSWA4'), ('Gestão de Projetos')])
    submit = SubmitField('Submit')

#Para que os campos dos formulários sejam exibidos ao enviar os dados:
@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()

    if form.validate_on_submit():
        old_name = session.get('name')
        session['name'] = form.name.data
        session['sobrenome'] = form.sobrenome.data
        session['disciplina'] = form.disciplina.data
        session['inst_ens'] = form.inst_ens.data
        return redirect(url_for('index'))
    return render_template('index.html',
                            form=form,
                            name = session.get('name'),
                            sobrenome = session.get('sobrenome'),
                            disciplina = session.get('disciplina'),
                            inst_ens = session.get('inst_ens'),
                            current_time=datetime.utcnow()
                            )

@app.route('/')
def contexto():
    return render_template(
        'index.html',
        ip=request.remote_addr,
        host=request.host
    )

class LoginFormulario(FlaskForm):
    user = StringField(
        '',
        validators=[DataRequired()],
        render_kw={"placeholder": "Usuário ou e-mail"}
    )
    senha = PasswordField(
        '',
        validators=[DataRequired()],
        render_kw={"placeholder": "Informe a sua senha"}
    )
    enviar = SubmitField('Enviar')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginFormulario()
    if form.validate_on_submit():
        session['usuario_login'] = form.user.data
        return redirect(url_for('loginResponse'))

    return render_template('login.html', form=form, current_time=datetime.utcnow())

@app.route('/loginResponse')
def loginResponse():
    usuario = session.get('usuario_login', '')

    return render_template(
        'loginResponse.html',
        usuario=usuario,
        current_time=datetime.utcnow()
    )

