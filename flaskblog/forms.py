from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Optional
from flaskblog.models import User

#Inherit FlaskForm
class RegistrationForm(FlaskForm):
    username = StringField('Username',
                            validators=[DataRequired(),Length(min(2, 20))] )

    email = StringField('Email',
                            validators=[DataRequired(),Email()] )
                                
    password = PasswordField('Password',
                            validators=[DataRequired()] )    

    confirm_password = PasswordField('Confirm Password',
                            validators=[DataRequired(),EqualTo('password')])       

    submit = SubmitField('Sign up') 

    def validate_username(self,username):
        user = User.query.filter_by(username=username.data).first()

        # I don't know why validators of username above cannot limit the word sequence, so I did this
        if len(username.data) > 20  or len(username.data) < 2:
            raise ValidationError('The username must be at length 2 to 20')

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


class UpdateAccountForm(FlaskForm):

    #Validator : optional allows empty field
    username = StringField('Username',
                           validators=[Length(min=2, max=20), Optional()])
    email = StringField('Email',
                        validators=[Email(), Optional()])

    # Allow only jpg, png
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')


    def validate_username(self,username):

        if username.data != current_user.username :           
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username was already taken')


    def validate_email(self,email):

        if email.data != current_user.email :
            user = User.query.filter_by(email=email.data).first()            
            if user:
                raise ValidationError('That Email was already taken')            

class PostForm(FlaskForm):

    #Validator : optional allows empty field
    title = StringField('Title',
                           validators=[DataRequired(),Length(min=1)])

    content = TextAreaField('Content',
                        validators=[DataRequired(),Length(min=3)])

    submit = SubmitField('Post!')


class RequestPasswordForm(FlaskForm):

    email = StringField('Email',
                            validators=[DataRequired(),Email()] )
                                
    submit = SubmitField('Request') 

    def validate_email(self,email):
        email = User.query.filter_by(email=email.data).first()

        if email is None:
            raise ValidationError('There is no email like this, please register it')

class ResetPasswordForm(FlaskForm):

    password = PasswordField('Password',
                            validators=[DataRequired()] )    

    confirm_password = PasswordField('Confirm Password',
                            validators=[DataRequired(),EqualTo('password')])       

    submit = SubmitField('Reset') 