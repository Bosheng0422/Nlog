import os
WTF_CSRF_ENABLED = True

# secret-key changed to a complex one
SECRET_KEY = 'secret-ss-kkkey024244500keysffsf'

basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db') 
SQLALCHEMY_TRACK_MODIFICATIONS = True 
