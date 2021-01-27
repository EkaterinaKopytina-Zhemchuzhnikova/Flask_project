from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField, StringField
from wtforms.validators import DataRequired


class Proposal(FlaskForm):
    username = StringField('Введите ФИО', validators=[DataRequired()])
    password = PasswordField('Введите СНИЛС', validators=[DataRequired()])
    telephone = StringField('Введите контактный номер', validators=[DataRequired()])
    submit = SubmitField('Отправить заявку')
