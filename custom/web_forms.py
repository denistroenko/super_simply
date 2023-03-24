"""
custom forms module
"""


from flask import request, session
from flask_wtf import FlaskForm as Form
from wtforms import StringField, SubmitField, HiddenField
from wtforms.widgets import TextArea
from wtforms.validators import DataRequired, Email

# Форма обратной связи
class FeedBackForm(Form):
    # Fields
    name = StringField('Имя', validators=[DataRequired()])  # Name
    second_name = StringField('Отчество')                   # Second name
    last_name = StringField('Фамилия')                      # Last Name
    phone = StringField('Телефон', validators=[DataRequired()])         # Phone
    email = StringField('email', validators=[DataRequired(), Email()])  # Email
    submit = SubmitField('Отправить')                       # Submit
    message = StringField('Сообщение', widget=TextArea())   # Message text
    # Hidden fields
    url = HiddenField()                                     # url
    base_url = HiddenField()                                # base_url
    page_name = HiddenField()                               # Page name
    choice = HiddenField()                                  # Choice


def get_forms() -> dict:
    """
    return dict custom forms
    """
    feedback_form = FeedBackForm()
    feedback_form.url.data = request.url
    feedback_form.base_url.data = request.base_url

    try:
        feedback_form.page_name.data = session['page.name']
    except KeyError:
        feedback_form.page_name.data  = '?'

    forms = {'feedback': feedback_form,
             }

    return forms
