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
    name = StringField('Qual é o seu nome?', validators=[DataRequired()])
    funcao = SelectField('Qual a sua função?', choices=[('User', 'User'), ('Administrator', 'Administrator'), ('Moderator', 'Moderator')])
    submit = SubmitField('Submit')


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
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


@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        #verifica se o usuário existe
        user = User.query.filter_by(username=form.name.data).first()
        #se não existir:
        if user is None:
            #encontra a função selecionada no selectField
            user_role = Role.query.filter_by(name=form.funcao.data).first()
            #se a função ainda não existir no BD, cria ela
            if user_role is None:
                user_role = Role(name=form.funcao.data)
                db.session.add(user_role)
            #cria as informações do usuário
            user = User(username=form.name.data, role=user_role)
            #adiciona o usuário no BD
            db.session.add(user)
            db.session.commit()
            session['known'] = False
        else:
            session['known'] = True

        session['name'] = form.name.data
        session['funcao'] = form.funcao.data
        return redirect(url_for('index'))
    #Conta a quantidade de users e roles existentes
    qtdUsers = User.query.count()
    qtdRoles = Role.query.count()

    #Encontra o nome das roles
    roles = Role.query.order_by(Role.id).all()

    #Encontra todos os usuários
    users = User.query.order_by(User.id).all()

    #A função selecionada é guardada
    funcaoDaSessao = session.get('funcao')
    #filtra pelo nome da função, ignorando caracteres maiúsculos e minúsculos por utilizar ilike
    userRole = Role.query.filter(Role.name.ilike(funcaoDaSessao)).first() if funcaoDaSessao else None


    return render_template(
        'index.html',
        form=form,
        name=session.get('name'),
        known=session.get('known', False),
        current_time=datetime.utcnow(),
        users=users,
        roles=roles,
        qtdUsers=qtdUsers,
        qtdRoles=qtdRoles,
        userRole=userRole
   )
