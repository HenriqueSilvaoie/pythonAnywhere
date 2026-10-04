from flask import Flask, render_template, session, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_moment import Moment, datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField
from wtforms.validators import DataRequired
import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

project_folder = os.path.expanduser('~/flasky')
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(project_folder, '.env'))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Abidi@1329'
bootstrap = Bootstrap(app)
moment = Moment(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

app.config['API_KEY'] = os.environ.get('API_KEY')
app.config['API_URL'] = os.environ.get('API_URL')
app.config['API_FROM'] = os.environ.get('API_FROM')

app.config['FLASKY_MAIL_SUBJECT_PREFIX'] = '[Flasky]'
app.config['FLASKY_ADMIN'] = os.environ.get('FLASKY_ADMIN')

class NameForm(FlaskForm):
    name = StringField('Qual é o seu nome?', validators=[DataRequired()])
    enviar_email = BooleanField('Enviar e-mail para flaskaulasweb@zohomail.com')
    submit = SubmitField('Submit')


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.name

class EmailEnviado(db.Model):
    __tablename__= 'emails'
    id = db.Column(db.Integer, primary_key=True)
    remetente = db.Column(db.String(100))
    destinatarios = db.Column(db.String(300))
    assunto = db.Column(db.String(200))
    texto = db.Column(db.Text)
    data_hora = db.Column(db.DateTime, default=datetime.now)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<User %r>' % self.username

@app.route('/emailsEnviados')
def emailsEnviados():
    emails = EmailEnviado.query.order_by(EmailEnviado.data_hora.desc()).all()
    return render_template('email.html', emails=emails)

@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():

        destinatarios = [os.getenv('FLASKY_ADMIN')]
        user = User.query.filter_by(username=form.name.data).first()
        #se não existir:
        if user is None:

            user = User(username=form.name.data)

            db.session.add(user)
            db.session.commit()
            session['known'] = False
            if form.enviar_email.data:
                destinatarios.append(os.getenv('EMAIL_FABIO'))

            subject = 'Novo Cadastro'

            for destinatario in destinatarios:
               mensagem = Mail(
                from_email=os.getenv('API_FROM'),
                to_emails = destinatarios,
                subject=subject,
                html_content=f"""
                    <p><b>Nome cadastrado:</b> {user.username}</p>
                    <p><b>Prontuário:</b> PT3037461</p>
                    <p><b>Aluno:</b> Henrique Teodoro Silva</p>
                """
                )
            try:
                sg = SendGridAPIClient(os.getenv('API_KEY'))
                sg.send(mensagem)
                db.session.add(EmailEnviado(
                    remetente = user.username,
                    destinatarios = ", ".join(destinatarios),
                    assunto = subject,
                    texto = f'Novo usuário cadastrado: {user.username}'
                    ))
                db.session.commit()

            except Exception as e:
                print(f"Erro ao enviar email pelo SendGrid: {e}")
        else:
            session['known'] = True

        session['name'] = form.name.data
        return redirect(url_for('index'))

    users=User.query.all()


    return render_template(
        'index.html',
        form=form,
        name=session.get('name'),
        known=session.get('known', False),
        current_time=datetime.utcnow(),
        users=users
   )







