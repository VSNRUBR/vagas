from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError

db = SQLAlchemy()

class Vaga(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    empresa = db.Column(db.String(50), nullable=False)
    vaga = db.Column(db.String(50), nullable=False)
    data = db.Column(db.Date)
    link = db.Column(db.String(128), nullable=False)


class User(db.Model, UserMixin):
    __bind_key__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)


class RegisterForm(FlaskForm):
    username = StringField(
        validators=[InputRequired(), Length(min=4, max=20)],
        render_kw={'placeholder': 'Nome de usuario'}
    )
    password = PasswordField(
        validators=[InputRequired(), Length(min=4, max=20)],
        render_kw={'placeholder': 'Senha'}
    )
    submit = SubmitField('Registrar')

    def validate_username(self, username):
        existing_user_username = User.query.filter_by(username=username.data).first()
        if existing_user_username:
            raise ValidationError('Nome de usuario ja registrado.')


class LoginForm(FlaskForm):
    username = StringField(
        validators=[InputRequired(), Length(min=4, max=20)],
        render_kw={'placeholder': 'Nome de usuario'}
    )
    password = PasswordField(
        validators=[InputRequired(), Length(min=4, max=20)],
        render_kw={'placeholder': 'Senha'}
    )
    submit = SubmitField('Login')
