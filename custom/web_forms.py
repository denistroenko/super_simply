"""
custom forms module
"""


from flask_wtf import FlaskForm as Form
from wtforms import StringField, SubmitField, HiddenField
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
    message = StringField('Сообщение')                      # Message text
    # Hidden fields
    page_url = HiddenField()                                # url
    page_name = HiddenField()                               # Page name
    choice = HiddenField()                                  # Choice


def get_forms() -> dict:
    """
    return dict custom forms
    """
    feedback_form = FeedBackForm()

    forms = {'feedback': feedback_form,}

    return forms
