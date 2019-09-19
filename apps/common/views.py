__author__ = 'yuchen'
__date__ = '2018/8/27 17:38'

from flask import Blueprint, make_response,request
from utils.captcha import Captcha
from io import BytesIO
from yunpian_python_sdk.model import constant as YC
from yunpian_python_sdk.ypclient import YunpianClient
from config import DevConfig
from utils import resful
import string
import random
from .forms import SmsCaptchaForm
from utils import landicache

bp=Blueprint('common',__name__,url_prefix='/c')



@bp.route('/')
def index():
    return 'common index'




@bp.route('/captcha/')
def graph_captcha():
    #调用得到验证码
    text,image=Captcha.gene_graph_captcha()
    #bytesIO二进制流
    out=BytesIO()
    image.save(out,'png')
    out.seek(0)
    resp=make_response(out.read())
    resp.content_type='image/png'
    print('前端生成的图形验证码是',text.lower())
    landicache.set(text.lower(),text.lower())
    print('后端生成的图形验证码',landicache.get(text.lower()))
    return resp

def get_back_random_cptcha():
    source = list(string.ascii_letters)
    source.extend(map(lambda x: str(x), range(0, 10)))

    # 还有一种写法,但是太low了
    # source.extend(['0','1','2','3','4','5','6','7','8','9','10'])
    random_code_captcha = random.sample(source, 4)
    captcha_code = ''.join(random_code_captcha)
    return captcha_code

@bp.route('/sms_captcha/',methods=['POST'])
def sms_captcha():
    form=SmsCaptchaForm(request.form)
    if form.validate():
        telephone=form.telephone.data
        captcha=get_back_random_cptcha()
        print('电话号码是',telephone)
        print('发送给用户的短信验证码是',captcha)
        #在memcache里存telephone和验证码
        landicache.set(telephone,captcha.lower())
        # message='【雨晨论坛】您的验证码是{}。如非本人操作，请忽略本短信'.format(captcha)
        # clnt = YunpianClient(DevConfig.YUNPIAN_CODE)
        # param = {YC.MOBILE: telephone, YC.TEXT: message}
        # if clnt.sms().single_send(param):
        #     #在memcache里存telephone和验证码
        #     landicache.set(telephone,captcha.lower())
        #     return resful.success('短信验证码发送成功')
        # else:
        #     return resful.params_error(message='请传入手机号码')
        return resful.success('短K信验证码发送成功')
    else:
        return resful.params_error(message='参数错误')
        # return resful.success('曾博的成功')

