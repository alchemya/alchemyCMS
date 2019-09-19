__author__ = 'yuchen'
__date__ = '2018/8/27 17:35'


import os
from datetime import timedelta

class Config(object):
    pass

class ProdConfig(Config):
    pass

class DevConfig(Config):
    DEBUG= False
    USERNAME = 'root'
    PASSWORD = 'angie'
    HOSTNAME = '127.0.0.1'
    PORT = '3306'
    DATABASE = 'LandiCMS'
    DB_URI = "mysql+pymysql://{username}:{password}@{host}:{port}/{db}?charset=utf8".format(username=USERNAME,
                                                                                            password=PASSWORD,
                                                                                            host=HOSTNAME, port=PORT,
                                                                                            db=DATABASE)
    SQLALCHEMY_DATABASE_URI = DB_URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # DEBUG = True
    PERMANENT_SESSION_LIFETIME = timedelta(days=8)

    # SECRET_KEY = os.urandom(24)
    SECRET_KEY='yawenxiaojiejie'
    YUNPIAN_CODE='ddad7d6a0a582ae5a022f93b1c355494'
    MAIL_SERVER = 'smtp.qq.com'
    MAIL_PORT = '465'
    MAIL_USE_SSL = True  # 使用SSL，端口号为465或587
    MAIL_USERNAME = '1005862748@qq.com'
    MAIL_PASSWORD = 'rhxcanfhkockbfdf'  # 注意，这里的密码不是邮箱密码，而是授权码
    MAIL_DEFAULT_SENDER = '1005862748@qq.com'  # 默认发送者

    # MAIL_USE_TLS：端口号587
    # MAIL_USE_SSL：端口号465
    # QQ邮箱不支持非加密方式发送邮件
    # 发送者邮箱的服务器地址

    PER_PAGE = 10



CMS_USER_ID='wnsgdsb'
FRONT_USER_ID='higirl'
UEDITOR_UPLOAD_TO_QINIU = True
UEDITOR_QINIU_ACCESS_KEY = '7wL2HnNizlF2OCeFGkmu2KdMG0exOXsA5GQi8EMT'
UEDITOR_QINIU_SECRET_KEY = 'fYQ30QziTfynz-osSuoq6pA7xewupEy764l6Zxgl'
UEDITOR_QINIU_BUCKET_NAME = 'images'
UEDITOR_QINIU_DOMAIN = 'http://pem47mau1.bkt.clouddn.com/'