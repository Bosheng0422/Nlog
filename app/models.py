'''
Author: your name
Date: 2020-12-28 09:57:27
LastEditTime: 2021-01-14 16:58:17
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: \COMP2011\2011cw2\app\models.py
'''
from app import db
from datetime import datetime



collect_article =db.Table('collect_article',db.Model.metadata,
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('articles_id', db.Integer, db.ForeignKey('article.id'))
)

# database model
class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime,default=datetime.strptime(datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),"%Y-%m-%d %H:%M:%S"))
    author_name = db.Column(db.String(100))
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    title = db.Column(db.String(100))
    content = db.Column(db.String(20000))
    image = db.Column(db.String(200))
    comments = db.relationship('Comment', backref='article', lazy='dynamic')
    users = db.relationship('User', secondary=collect_article)
        
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    writer = db.Column(db.String(30))
    content = db.Column(db.String(150))
    time = db.Column(db.DateTime,default=datetime.strptime(datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),"%Y-%m-%d %H:%M:%S"))
    article_id = db.Column(db.Integer, db.ForeignKey('article.id'))
    replies = db.relationship('CommentReply', backref='comment', lazy='dynamic')

        
class CommentReply(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    writer = db.Column(db.String(30))
    content = db.Column(db.String(150))
    time = db.Column(db.DateTime,default=datetime.strptime(datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),"%Y-%m-%d %H:%M:%S"))
    comment_id = db.Column(db.Integer, db.ForeignKey('comment.id'))


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(20))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    articles = db.relationship('Article', backref='category', lazy='dynamic')


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30))
    blogname = db.Column(db.String(30))
    password = db.Column(db.String(30))
    articles = db.relationship('Article', secondary=collect_article)
    categories = db.relationship('Category', backref='user', lazy='dynamic')
    
    