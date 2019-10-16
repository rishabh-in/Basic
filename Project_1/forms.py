from flask_wtf import FlaskForm
from wtforms import SubmitField,StringField,IntegerField

class AddForm(FlaskForm):

    name=StringField("Name of the Student")

    submit=SubmitField("Add")

class DelForm(FlaskForm):

    id=IntegerField("Id of the Student to be removed")

    submit=SubmitField("Remove")
