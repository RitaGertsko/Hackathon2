from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, RadioField, SubmitField, BooleanField
from wtforms.validators import Email, EqualTo, InputRequired, Optional, Length


class RegistrationForm(FlaskForm):
    first_name = StringField(label="First Name: ",
                             validators=[InputRequired(message='Please enter your first name'), Length(min=2, max=15)])
    last_name = StringField(label="Last Name: ", validators=[Optional(), Length(min=2, max=15)])
    email = EmailField(label="Email: ",
                       validators=[Email(message="Email incorrect: "), InputRequired(message='Please enter your email'),
                                   Length(min=2, max=50)])
    password = PasswordField(label="Password: ",
                             validators=[InputRequired(message='Please enter password'), Length(min=2, max=25)])
    confirm_password = PasswordField(label="Confirm Password: ",
                                     validators=[EqualTo('password', message='Passwords must match'), InputRequired()])
    age = RadioField(label="Age: ",
                     choices=[('14-20', '14-20'), ('20-30', '20-30'), ('30-40', '30-40'), ('40-50', '40-50'),
                              ('+50', '+50')], validators=[Optional()])
    submit = SubmitField(label='Sign up')


class LoginForm(FlaskForm):
    email = EmailField(label="Email: ",
                       validators=[Email(message="Email incorrect"), InputRequired(message='Please input your email'),
                                   Length(min=2, max=25)])
    password = PasswordField(label="Password: ",
                             validators=[InputRequired(message='Please enter password'), Length(min=2, max=20)])
    remember = BooleanField('Remember me')
    submit = SubmitField(label='Log in')


class SearchForm(FlaskForm):
    word = StringField(label="Search: ",
                       validators=[Length(min=2, max=25)])
    submit = SubmitField('submit')
