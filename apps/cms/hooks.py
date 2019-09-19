__author__ = 'yuchen'
__date__ = '2018/8/28 00:18'
from .views import bp
from config import CMS_USER_ID
from flask import session,g
from .models import CMSUser,CMSPermission

@bp.before_request
def before_request():
    if CMS_USER_ID in session:
        user_id=session.get(CMS_USER_ID)
        user=CMSUser.query.get(user_id)
        if user:
            g.cms_user=user

@bp.context_processor
def context_processor():
    return {'CMSPermission': CMSPermission}