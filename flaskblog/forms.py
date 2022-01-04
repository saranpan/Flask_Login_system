from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flaskblog.models import User

#Inherit FlaskForm
class RegistrationForm(FlaskForm):
    username = StringField('Username',
                            validators=[DataRequired(),Length(min(2, 20))] )

    email = StringField('Email',
                            validators=[DataRequired(),Email()] )
                                
    password = PasswordField('Password',
                            validators=[DataRequired()] )    

    confirm_password = StringField('Confirm Password',
                            validators=[DataRequired(),EqualTo('password')])       

    submit = SubmitField('Sign up') 

    def validate_username(self,username):
        user = User.query.filter_by(username=username.data).first()

        if user:
            raise ValidationError('This Username was already taken, please use another')

    def validate_email(self,email):
        email = User.query.filter_by(email=email.data).first()

        if email:
            raise ValidationError('This Email was already taken, please use another')




class LoginForm(FlaskForm):

    email = StringField('Email',
                            validators=[DataRequired(),Email()] )
                                
    password = PasswordField('Password',
                            validators=[DataRequired()] )    

    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')      