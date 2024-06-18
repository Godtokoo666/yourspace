# app/config.py
class Config:
    SITE_NAME = 'YourSpace'
    CRRUENT_YEAR = '2024'
    BABEL_DEFAULT_TIMEZONE='UTC+8'
    SECRET_KEY = '74052adb15762d5443f09ac68d28d6d6'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
