__author__ = 'yuchen'
__date__ = '2018/8/27 17:38'

from wtforms import StringField,IntegerField,ValidationError
from wtforms.validators import Email,InputRequired,Length,EqualTo,Regexp
from apps.common.forms import BaseForm
from .models import CMSUser
from utils import landicache
from flask import g
import types



class LoginForm(BaseForm):
    email=StringField(validators=[Email(message='请输入正确格式的邮箱'),InputRequired('请输入邮箱')])
    password=StringField(validators=[Length(6,20,message='请输入正确格式的密码')])
    remember=IntegerField()




class ResetpwdForm(BaseForm):
    oldpwd= StringField(validators=[Length(6,20,message='请输入格式正确的旧密码')])
    newpwd=StringField(validators=[Length(6,20,message='请输入格式正确的新密码')])
    newpwd2=StringField(validators=[EqualTo('newpwd',message='两次输入的密码不一致')])




class RestEmailForm(BaseForm):
    email=StringField(validators=[Email('邮箱格式错误'),InputRequired('请输入邮箱内容')])
    captcha = StringField(validators=[InputRequired('请输入验证码内容'),Length(6,6,message='请输入6位验证码')])

    #自定义验证器保证两次邮箱不一样
    def validate_email(self,field):
        old_email=g.cms_user.email
        print('a',self.email.data)
        print('b',field.data)
        print('g',g.cms_user.email)
        if field.data == old_email:
            raise ValidationError('输入了相同的邮箱')
    #保证缓存的验证码和输入的验证码一致
    def validate_captcha(self,field):
        email=self.email.data
        if email:
            captcha_cache=landicache.get(email)
            if captcha_cache is None or captcha_cache.lower() != field.data.lower():
                raise  ValidationError('验证码不对')
        else:
            raise ValidationError('请输入邮箱')


class AddBannerForm(BaseForm):
    name = StringField(validators=[InputRequired(message='请输入轮播图名称！')])
    image_url = StringField(validators=[InputRequired(message='请输入轮播图图片链接！')])
    link_url = StringField(validators=[InputRequired(message='请输入轮播图跳转链接！')])
    priority = StringField(validators=[InputRequired(message='请输入轮播图优先级！'),Regexp(r'^(0|[1-9][0-9]*)$',
                                                                                  message='优先级请以数字表示')])


class UpdateBannerForm(AddBannerForm):
    banner_id = IntegerField(validators=[InputRequired(message='请输入轮播图的id')])


class AddBoardsForm(BaseForm):
    name=StringField(validators=[InputRequired(message='请输入版块名称'),Length(2,15,message='长度应在2-15个字符之间')])

class UpdateBoardForm(AddBoardsForm):
    board_id=IntegerField(validators=[InputRequired(message='请输入版块名称')])





















