from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, IntegerField, SubmitField, TextAreaField, BooleanField
from wtforms.validators import InputRequired, Optional, URL, NumberRange, Length

class PetForm(FlaskForm):
    name = StringField('Name',
                           validators=[InputRequired()])
    species = SelectField('Species',
                           choices=[("Cat", "Cat"), ("Dog", "Dog"), ("Porcupine", "Porcupine")])
    photo_url = StringField('Photo Url',
                            validators=[Optional(), URL()])
    age = IntegerField('Age',
                       validators=[Optional(), NumberRange(min=0, max=30)])
    notes = TextAreaField('Notes',
                          validators=[Optional(), Length(min=10, max=300)])
    available = BooleanField('Available')
    submit = SubmitField('Submit')