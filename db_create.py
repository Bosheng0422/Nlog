from config import SQLALCHEMY_DATABASE_URI
from app import db
import os.path

# create a database
db.create_all()