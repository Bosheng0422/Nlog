'''
Author: your name
Date: 2020-12-28 09:57:27
LastEditTime: 2021-01-12 06:43:39
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: \2011cw2\app\__init__.py
'''
# import the packages
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_admin import Admin

app = Flask(__name__)
admin = Admin(app,template_mode='bootstrap3')
# apply the config file setting
app.config.from_object('config') 
# database applied
db = SQLAlchemy(app) 
# migrate the db named app
migrate = Migrate(app, db, render_as_batch=True) 
from app import views, models