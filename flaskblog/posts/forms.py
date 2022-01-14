from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length

class PostForm(FlaskForm):

    #Validator : optional allows empty field
    title = StringField('Title',
                           validators=[DataRequired(),Length(min=1)])

    content = TextAreaField('Content',
                        validators=[DataRequired(),Length(min=3)])

    submit = SubmitField('Post!')
