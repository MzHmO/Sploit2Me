from wtforms import StringField, EmailField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, Email
from flask_wtf import FlaskForm


class RegistrationForm(FlaskForm):
    username = StringField("Логин", validators=[InputRequired(), Length(min=5, max=25)])
    email = EmailField("Почта", validators=[InputRequired(), Email()])
    password_1 = PasswordField("Пароль", validators=[InputRequired(), Length(min=5, max=25)])
    password_2 = PasswordField("Повторите пароль", validators=[InputRequired(), Length(min=5, max=25)])
    submit = SubmitField('Зарегистрироваться', id='submit-btn')


class LoginForm(FlaskForm):
    username = StringField("Логин", validators=[InputRequired(), Length(min=5, max=25)])
    password = PasswordField("Пароль", validators=[InputRequired(), Length(min=5, max=25)])
    submit = SubmitField('Войти', id='submit-btn')
