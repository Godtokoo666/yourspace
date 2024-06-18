#app/form.py
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, BooleanField, SelectField,IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Regexp, Optional,NumberRange
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
    title = StringField('Title', validators=[DataRequired(),Length(min=5, max=15)])
    content = TextAreaField('Content', validators=[DataRequired(),Length(max=2000)])
    node = SelectField('Node',choices=[],coerce=int,validators=[DataRequired()])
    submit = SubmitField('Post')
    
class CommentForm(FlaskForm):
    cid = IntegerField('Cid',validators=[Optional()])
    content = TextAreaField('Content', validators=[DataRequired(),Length(max=200)])
    submit = SubmitField('Comment')
    
    
class confirmForm(FlaskForm):
    submit = SubmitField('Confirm')
    
class SpaceForm(FlaskForm):
    avatar = StringField('Avatar')
    bio = TextAreaField('Bio')
    submit = SubmitField('Update')

class AdminUserForm(FlaskForm):
    uid = StringField('Uid', validators=[DataRequired()])
    level= IntegerField('Level',validators=[Optional(),NumberRange(min=0,max=5)])
    priv = IntegerField('Priv',validators=[Optional(),NumberRange(min=1,max=3)])
    banned_status = IntegerField('Banned Status',validators=[Optional(),NumberRange(min=0,max=5)])
    submit = SubmitField('Update')

class AdminNodeForm(FlaskForm):
    
    nid = IntegerField('Nid', validators=[Optional()])
    name = StringField('Name',validators=[Optional()])
    description = StringField('Description',validators=[Optional()])
    url= StringField('Url',validators=[Optional()])
    access_level = IntegerField('Access Level',validators=[Optional(),NumberRange(min=0,max=5)])
    avatar = StringField('Avatar',validators=[Optional()])
    parent = IntegerField('Parent',validators=[Optional()])
    submit = SubmitField('Update')
    
class AdminPostForm(FlaskForm):
    pid= StringField('Pid', validators=[DataRequired()])
    node=IntegerField('Node',validators=[Optional()])
    access_level = IntegerField('Access Level',validators=[Optional(),NumberRange(min=0,max=5)])
    topped = BooleanField('Topped',default=False)
    readonly = BooleanField('Readonly',default=False)
    sort = IntegerField('Sort',validators=[Optional()])
    submit = SubmitField('Update')
    
class dashboardForm(FlaskForm):
    site_name = StringField('Site Name')
    logo = StringField('Logo')
    base_url = StringField('Base Url')
    background_url = StringField('Background')
    site_closed = BooleanField('Site Closed')
    register_open = BooleanField('Register Open')
    submit = SubmitField('Dashboard')

    
