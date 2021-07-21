from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, EqualTo

class RegistrationForm(FlaskForm):

    user_name = StringField('username',validators=[InputRequired(message="Username Required"),
    Length(min=4,max=20, message="Username must be Minimum 4 char long.")])
    
    pass_word = PasswordField('pass',validators=[InputRequired(message="Password Required"),
    Length(min=4,max=8, message="Password Must Be 4 char long.")])
    
    con_pass = PasswordField('cpass',validators=[InputRequired(message="Password Required"),EqualTo("pass_word", message="Password Must Match.")]) 
    
    sub_btn = SubmitField('Register')