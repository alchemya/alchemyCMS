__author__ = 'yuchen'
__date__ = '2018/8/27 17:38'

from exts import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


# 用户表
class CMSUser(db.Model):
    __tablename__ = 'cms_user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False)
    _password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    join_time = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, username, password, email):
        self.username = username
        self.password = password  # 新定义的setter方法被调用了
        self.email = email

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, raw_password):
        self._password = generate_password_hash(raw_password)

    def check_password(self, raw_password):
        result = check_password_hash(self.password, raw_password)
        # print('结果呢',result)
        return result

    @property
    def permissions(self):
        # 如果该用户没有任何角色，则没有权限
        if not self.roles:
            return 0
        # 遍历该用户拥有的角色，获取该角色权限，并所有所含所有角色权限通过或运算组合在一起
        all_permissions = 0
        for role in self.roles:
            permissions = role.permissions
            all_permissions |= permissions
        return all_permissions

    def has_permission(self, permission):
        # 把传过来的权限和该用户所拥有的权限进行与运算，得出的结果和传过来的权限进行比较，一致的话则拥有该权限
        #  0b00000011 & 0b00000001 ---->1 (0b00000001)
        # all_permissions=self.permissions
        # result = all_permissions & permission == permission
        # return result
        return self.permissions & permission == permission

    @property
    def is_developer(self):
        # 判断该用户是否是开发者，开发者拥有所有权限
        return self.has_permission(CMSPermission.ALL_PERMISSION)


class CMSPermission(object):
    # 255的二进制方式表示11111111
    ALL_PERMISSION = 0b11111111
    # 访问者权限
    VISITOR = 0b00000001
    # 管理帖子权限
    POSTER = 0b00000010
    # 管理评论的权限
    COMMENTER = 0b00000100
    # 管理板块的权限
    BOARDER = 0b00001000
    # 管理前台用户的权限
    FRONTUSER = 0b00010000
    # 管理后台用户的权限
    CMSUSER = 0b00100000
    # 管理所有管理员的权限
    ADMIN = 0b01000000


cms_role_user = db.Table(
    'cms_role_user',
    db.Column('cms_role_id', db.Integer, db.ForeignKey('cms_role.id'), primary_key=True),
    db.Column('cms_user_id', db.Integer, db.ForeignKey('cms_user.id'), primary_key=True)
)


# 角色表
class CMSRole(db.Model):
    __tablename__ = 'cms_role'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    desc = db.Column(db.String(200), nullable=True)
    create_time = db.Column(db.DateTime, default=datetime.now)
    permissions = db.Column(db.Integer, default=CMSPermission.VISITOR)
    users = db.relationship('CMSUser', secondary=cms_role_user, backref='roles')




