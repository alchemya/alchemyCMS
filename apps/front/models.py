__author__ = 'yuchen'
__date__ = '2018/8/27 17:38'


from exts import db
import shortuuid
from werkzeug.security import generate_password_hash, check_password_hash
import enum
from datetime import datetime

class GenderEnum(enum.Enum):
    MALE = 1
    FEMALE = 2
    SECRET = 3
    UNKNOW = 4



class FrontUser(db.Model):
    __tablename__ = 'front_user'
    #这里的id如果我们还使用自动增长，就会存在商业安全隐患，用户可以根据id推算出我们网站的人数
    #不使用自动增长，又要保证id的唯一性，我们就可以使用uuid
    #虽然uuid好用，但是它太长了，查找的效率会降低
    #这时我们就可以使用shortuuid这个库，它既满足了唯一性，又没有uuid那么长
    id = db.Column(db.String(100), primary_key=True, default=shortuuid.uuid)
    telephone = db.Column(db.String(11), nullable=False)
    username = db.Column(db.String(50), nullable=False)
    _password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(50), unique=True)
    realname = db.Column(db.String(50))
    avatar = db.Column(db.String(50))#头像
    signature = db.Column(db.String(100))#签名
    gender = db.Column(db.Enum(GenderEnum), default=GenderEnum.UNKNOW)
    join_time = db.Column(db.DateTime, default=datetime.now)

    #对password对应的是_password，所以要做处理
    def __init__(self, *args, **kwargs):
        if "password" in kwargs:
            self.password = kwargs.get('password')
            kwargs.pop("password")
        super(FrontUser, self).__init__(*args, **kwargs)


    @property
    def password(self):
        return self._password



    @password.setter
    def password(self, newpwd):
        self._password = generate_password_hash(newpwd)

    def check_password(self, rawpwd):
        return check_password_hash(self._password, rawpwd)

class BannerModel(db.Model):
    __tablename__ = 'banner'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    image_url = db.Column(db.String(255), nullable=False)
    link_url = db.Column(db.String(255), nullable=False)
    priority = db.Column(db.Integer, default=0)
    create_time = db.Column(db.DateTime, default=datetime.now)


class BoardModel(db.Model):
    __tablename__ = 'board'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)





class PostModel(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    board_id = db.Column(db.Integer, db.ForeignKey('board.id'))
    board = db.relationship('BoardModel', backref='posts')
    author_id = db.Column(db.String(50), db.ForeignKey('front_user.id'), nullable=False)
    author = db.relationship('FrontUser', backref='posts')
    reading_count=db.Column(db.BigInteger,default=0,nullable=False)



class CommentModel(db.Model):
    __tablename__='comment'
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    content=db.Column(db.Text,nullable=False)
    create_time=db.Column(db.DateTime,default=datetime.now)
    post_id=db.Column(db.Integer,db.ForeignKey('post.id'))
    author_id = db.Column(db.String(50), db.ForeignKey('front_user.id'), nullable=False)

    post=db.relationship('PostModel',backref='comments')
    author=db.relationship('FrontUser',backref='comments')


class HighLight(db.Model):
    __tablename__='highlight_post'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    post_id=db.Column(db.Integer,db.ForeignKey('post.id'))
    create_time=db.Column(db.DateTime,default=datetime.now)

    post=db.relationship('PostModel',backref='highlight')


