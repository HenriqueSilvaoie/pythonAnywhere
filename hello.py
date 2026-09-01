from flask import Flask, render_template, request, session, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_moment import Moment, datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, PasswordField
from wtforms.validators import DataRequired
import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Abidi@1329'
bootstrap = Bootstrap(app)
moment = Moment(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.name

class User(db.Model):
  __tablename__ = 'users'
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(64), unique=True, index=True)
  role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
  def __repr__(self):
    return '<User %r>' % self.username

@app.shell_context_processor
def make_shell_context():
  return dict(db=db, User=User, Role=Role)


#Semana 07
@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            db.session.commit()
            session['known'] = False
        else:
            session['known'] = True
        session['name'] = form.name.data
        return redirect(url_for('index'))
    return render_template('index.html', form=form,
                            name=session.get('name'),
                            known=session.get('known', False),
                            current_time=datetime.utcnow())

#Para que os campos dos formulários sejam exibidos ao enviar os dados:
#@app.route('/', methods=['GET', 'POST'])
#def index():
#    form = NameForm()
    #if form.validate_on_submit():
     #   session['name'] = form.name.data
      #  session['sobrenome'] = form.sobrenome.data
       # session['disciplina'] = form.disciplina.data
        #session['inst_ens'] = form.inst_ens.data
        #return redirect(url_for('index'))
    #return render_template('index.html',
     #                       form=form,
      #                      name = session.get('name'),
       #                     sobrenome = session.get('sobrenome'),
        #                    disciplina = session.get('disciplina'),
         #                   inst_ens = session.get('inst_ens'),
          #                  current_time=datetime.utcnow()
           #                 )



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

