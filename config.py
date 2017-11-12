# import os


class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:wbh673406316@localhost:3306/board?charset=utf8'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SECRET_KEY = 'hard to guess in the future'
    ADMIN = '我'
