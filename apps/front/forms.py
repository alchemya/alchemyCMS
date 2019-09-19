__author__ = 'yuchen'
__date__ = '2018/8/27 17:39'

from apps.common.forms import BaseForm
from wtforms import StringField,IntegerField
from wtforms.validators import Regexp, Length, EqualTo, ValidationError,InputRequired,DataRequired
from utils import landicache
from .models import FrontUser
from config import FRONT_USER_ID





class IForgetForm(BaseForm):
    telephone = StringField(validators=[Regexp(r'1[35678]\d{9}', message='手机号码格式错误'),DataRequired(message='请输入空缺手机号')])
    sms_captcha = StringField(validators=[Regexp(r'\w{4}', message='短信验证码错误'),DataRequired(message='请输入短信验证码')])
    password1 = StringField(validators=[Regexp(r'^(?![0-9]+$)(?![a-zA-Z]+$)[0-9A-Za-z]{6,16}$',
                                               message='密码需要6位以上数字和字母的组合'),DataRequired(message='请输入空缺密码内容')])
    password2 = StringField(validators=[EqualTo('password1', message='两次密码不一致'),DataRequired(message='请重复输入密码')])
    graph_captcha = StringField(validators=[Regexp(r'\w{4}', message='图形验证码错误'),DataRequired(message='请输入图形验证码')])



    def validate_telephone(self, field):
        user = FrontUser.query.filter_by(telephone=field.data).first()
        if not user:
            raise ValidationError('该手机号未被注册')


    def validate_sms_captcha(self, field):
        telephone = self.telephone.data
        sms_captcha = field.data

        sms_captcha_restore = landicache.get(telephone)
        print('用户输入的短信验证码：{}'.format(sms_captcha))
        print('服务器存储的短信验证码：{}'.format(sms_captcha_restore))
        if not sms_captcha_restore or sms_captcha_restore != sms_captcha.lower():
            raise ValidationError(message='短信验证码错误')

    def validate_graph_captcha(self, field):
        graph_captcha = field.data
        print('用户输入的图形验证码是', graph_captcha)
        # 因为图形验证码存储的key和值都是一样的，所以我们只要判断key是否存在就行
        if not landicache.get(graph_captcha.lower()):
            raise ValidationError(message='图形验证码错误')


class SignUpForm(BaseForm):
    telephone = StringField(validators=[Regexp(r'1[35678]\d{9}',message='手机号码格式错误')])
    sms_captcha = StringField(validators=[Regexp(r'\w{4}', message='短信验证码错误')])
    username = StringField(validators=[Length(2,20, message='用户名格式错误')])
    password1 = StringField(validators=[Regexp(r'^(?![0-9]+$)(?![a-zA-Z]+$)[0-9A-Za-z]{6,16}$',
                                               message='密码需要6位以上数字和字母的组合')])
    password2 = StringField(validators=[EqualTo('password1', message='两次密码不一致')])
    graph_captcha = StringField(validators=[Regexp(r'\w{4}', message='图形验证码错误')])

    def validate_telephone(self, field):
        user = FrontUser.query.filter_by(telephone=field.data).first()
        if user:
            raise ValidationError('该手机号已被注册')

    def validate_sms_captcha(self, field):
        telephone = self.telephone.data
        sms_captcha = field.data

        sms_captcha_restore = landicache.get(telephone)
        print('用户输入的短信验证码：{}'.format(sms_captcha))
        print( '服务器存储的短信验证码：{}'.format(sms_captcha_restore))
        if not sms_captcha_restore or sms_captcha_restore != sms_captcha.lower():
            raise ValidationError(message='短信验证码错误')

    def validate_graph_captcha(self, field):
        graph_captcha = field.data
        print('用户输入的图形验证码是',graph_captcha)
        #因为图形验证码存储的key和值都是一样的，所以我们只要判断key是否存在就行
        if not landicache.get(graph_captcha.lower()):
            raise ValidationError(message='图形验证码错误')

class LoginForm(BaseForm):
    telephone = StringField(validators=[Regexp(r'1[35678]\d{9}', message='手机号码格式错误')])
    password=StringField(validators=[Length(6,20,message='请输入正确格式的密码')])
    remember=IntegerField()


class AddPostForm(BaseForm):
    title=StringField(validators=[InputRequired(message='请输入标题')])
    content=StringField(validators=[InputRequired(message='请输入内容')])
    board_id=IntegerField(validators=[InputRequired(message='请选择版块')])

class AddCommentForm(BaseForm):
    content=StringField(validators=[InputRequired(message='请输入评论内容')])
    post_id=IntegerField(validators=[InputRequired(message='请输入评论内容')])


