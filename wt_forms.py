from models import User
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, EqualTo, ValidationError
from passlib.hash import pbkdf2_sha256
from models import User

def check_data(form,passdata):
    username_login = form.user_name.data
    password_login = passdata.data

    user_object = User.query.filter_by(usernm=username_login).first()
    if user_object is None:
        raise ValidationError("Username or password is incorrect")
    elif not pbkdf2_sha256.verify(password_login,user_object.passw):
        raise ValidationError("Username or password is incorrect")

class RegistrationForm(FlaskForm):

    user_name = StringField('username',validators=[InputRequired(message="Username Required"),
    Length(min=4,max=20, message="Username must be Minimum 4 char long.")])
    
    pass_word = PasswordField('pass',validators=[InputRequired(message="Password Required"),
    Length(min=4,max=8, message="Password Must Be 4 char long.")])
    
    con_pass = PasswordField('cpass',validators=[InputRequired(message="Password Required"),EqualTo("pass_word", message="Password Must Match.")]) 
    
    sub_btn = SubmitField('Register')

    def validate_user_name(self, user_name):
        if User.query.filter_by(usernm=user_name.data).first():
            raise ValidationError("Username Already Exists...")


class LoginForm(FlaskForm):

    user_name = StringField('username',validators=[InputRequired(message="Username Required")])
    pass_word = PasswordField('pass',validators=[InputRequired(message="Password Required"),check_data])

    sub_btn = SubmitField('Login')
