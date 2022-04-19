import os
from random import randint

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = ''.join([chr(randint(97, 122)) for _ in range(256)])
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(basedir, 'shop.db')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
