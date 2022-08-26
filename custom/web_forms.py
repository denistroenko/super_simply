"""
Модуль описывает стандартные предустановленные формы
"""


from flask_wtf import FlaskForm as Form
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


# Форма обратной связи
class FeedBackForm(Form):
    # Fields
    name = StringField('Имя', validators=[DataRequired()])
    second_name = StringField('Отчество')
    last_name = StringField('Фамилия')
    phone = StringField('Телефон', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired()])
    submit = SubmitField('Отправить')
    message = StringField('Сообщение')

def get_forms() -> tuple:
    """
    Возвращает кортеж из 2-х элементов:
    1 - словарь forms {имя:форма}
    2 - словарь session {имя:данные}
    """
    feedback_form = FeedBackForm()

    forms = {'feedback': feedback_form,}

    session = {}
    session['name'] = feedback_form.name.data
    session['second_name'] = feedback_form.second_name.data
    session['last_name'] = feedback_form.last_name.data
    session['phone'] = feedback_form.phone.data
    session['email'] = feedback_form.email.data
    session['message'] = feedback_form.message.data

    return forms, session
