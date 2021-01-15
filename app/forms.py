'''
Author: your name
Date: 2020-12-28 09:57:27
LastEditTime: 2021-01-14 15:42:15
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: \2011cw2\app\forms.py
'''
from flask_wtf import FlaskForm
from wtforms import TextAreaField, StringField, PasswordField, DateTimeField, IntegerField
from wtforms.validators import DataRequired, Length, EqualTo
from flask_wtf.file import FileField, FileRequired, FileAllowed



class ArticleForm(FlaskForm):
    head = TextAreaField('head', render_kw={'placeholder': "Input your article title"} 
            , validators=[DataRequired()])
    content = TextAreaField('content', render_kw={'placeholder': "Input your article content"} 
                , validators=[DataRequired()])
    image = FileField('image', validators=[FileRequired(),
                FileAllowed(['jpg','jpeg','png','gif'], message="select file in jpg, jepg, png and gif")])
    category = IntegerField('category', validators=[DataRequired()] )
class CommentForm(FlaskForm):
    content = TextAreaField('content', render_kw={'placeholder': "Input your comment"} , validators=[DataRequired()])
    
class ReplyForm(FlaskForm):
    content = TextAreaField('content', render_kw={'placeholder': "Input your reply"} , validators=[DataRequired()])

class UserForm(FlaskForm):
    username = StringField('username', render_kw={'placeholder': "Username"} , validators=[DataRequired(message='username cannot be empty')])
    password = PasswordField('password', render_kw={'placeholder': "Password"} , validators=[DataRequired('password cannot be empty')])
    blogname = StringField('blogname', render_kw={'placeholder': "Blogname"} , validators=[DataRequired('blogname cannot be empty')])
    re_password = PasswordField('re_password',  render_kw={'placeholder': 'Confirm Password'},
                                            validators=[
                                                    DataRequired(message='confirm password cannot be empty'),
                                                    EqualTo('password', message='two passwords do not match')
                                                    ])