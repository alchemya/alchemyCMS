__author__ = 'yuchen'
__date__ = '2018/8/27 23:04'
from functools import wraps
from flask import session,url_for,redirect,g
import config

def login_required(func):
    @wraps(func)
    def inner(*args,**kwargs):
        if config.CMS_USER_ID  in session:
            return func(*args,**kwargs)
        else:
            return redirect(url_for('cms.login'))
    return inner


def permission_required(permission):
    def outter(func):
        @wraps(func)
        def inner(*args, **kwargs):
            #判断该用户是否有权限
            if g.cms_user.has_permission(permission):
                return func(*args, **kwargs)
            else:
                #没有权限则返回到首页
                return redirect(url_for('cms.index'))
        return inner
    return outter


