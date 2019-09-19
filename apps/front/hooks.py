__author__ = 'yuchen'
__date__ = '2018/9/6 19:04'

from .views import bp
from flask import session,g,request,render_template
from .models import FrontUser,BoardModel
import config

@bp.before_request
def before_request():
    if config.FRONT_USER_ID in session:
        user_id=session.get(config.FRONT_USER_ID)
        user=FrontUser.query.get(user_id)
        if user:
            g.front_user=user



