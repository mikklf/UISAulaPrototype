from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, HiddenField
from wtforms.validators import DataRequired, Length

class AddUserForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Add')

class UserLoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class SendMessageForm(FlaskForm):
    besked = StringField('Besked', validators=[DataRequired()])
    submit = SubmitField('Send')

class CreateThreadForm(FlaskForm):
    group_id = HiddenField('GroupID', validators=[DataRequired()])
    title = StringField('Title', validators=[DataRequired()])
    submit = SubmitField()

class CreateGroupForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    hidden = BooleanField('Skjul gruppe')
    submit = SubmitField("Opret gruppe")

class CreatePostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = StringField('Indhold', validators=[DataRequired()])
    author_id = HiddenField('AuthorID', validators=[DataRequired()])
    group_id = HiddenField('GroupID', validators=[DataRequired()])
    submit = SubmitField("Opret opslag")

