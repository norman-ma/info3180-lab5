from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, SelectField, FileField, TextAreaField
from wtforms.validators import InputRequired, EqualTo
from validators import Unique
from models import UserProfile

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    
class SignUpForm(FlaskForm):
    firstname = StringField('FirstName', validators=[InputRequired()])
    lastname = StringField('LastName', validators=[InputRequired()])
    username = StringField('UserName', validators=[InputRequired(),Unique(UserProfile,UserProfile.username,message = 'There is already a profile with that username')])
    age = IntegerField('Age', validators=[InputRequired()])
    gender = SelectField('Gender', choices=[('M','Male'),('F','Female')], validators=[InputRequired()])
    profilePic = FileField(validators=[InputRequired()])
    biography = TextAreaField("Biography",  validators=[InputRequired()])