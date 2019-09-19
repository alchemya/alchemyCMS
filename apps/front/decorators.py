__author__ = 'yuchen'
__date__ = '2018/9/6 17:04'

from flask import session,redirect,url_for
from functools import wraps
import config


def login_requried(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
        if  config.FRONT_USER_ID in session:
            return func(*args,**kwargs)
        else:
            return redirect(url_for('front.login_in'))
    return wrapper