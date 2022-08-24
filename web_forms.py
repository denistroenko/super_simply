from flask_wtf import FlaskForm as Form
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class CallBackForm(Form):
    # Fields
    name = StringField('Имя', validators=[DataRequired()])
    submit = SubmitField('Перезвоните мне')
