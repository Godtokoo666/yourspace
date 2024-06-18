#app/form.py
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Regexp
from app.models import User


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20), Regexp('^[a-zA-Z0-9]*$', message='用户名只能包含字母和数字')])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=20)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('用户名已存在！')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('邮箱已存在！')
        
class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    node = StringField('Node', validators=[DataRequired()])
    submit = SubmitField('Post')
    
class CommentForm(FlaskForm):
    cid = StringField('Cid')
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Comment')
    
    
class confirmForm(FlaskForm):
    submit = SubmitField('Confirm')
    
class SpaceForm(FlaskForm):
    avatar = StringField('Avatar')
    bio = TextAreaField('Bio')
    submit = SubmitField('Update')