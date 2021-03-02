from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField,  SelectField, BooleanField
from wtforms.validators import InputRequired

#Form for just login
class UserForm(FlaskForm):
    username= StringField("Username", validators=[InputRequired()])
    password= PasswordField("Password", validators=[InputRequired()])

#Includes it all login, email, first_name, last_name
class RegisterForm(FlaskForm):
    username= StringField("Username", validators=[InputRequired()])
    password= PasswordField("Password", validators=[InputRequired()])
    email= StringField("Email", validators=[InputRequired()])
    first_name= StringField("First Name", validators=[InputRequired()])
    last_name= StringField("Last Name", validators=[InputRequired()])


class FeedbackForm(FlaskForm):
    title = StringField("Title", validators=[InputRequired()])
    content = StringField("Content", validators=[InputRequired()])