"""
custom forms module
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


def get_forms() -> dict:
    """
    return dict custom forms
    """
    feedback_form = FeedBackForm()

    forms = {'feedback': feedback_form,}

    return forms
