__author__ = 'yuchen'
__date__ = '2018/8/27 17:39'
from wtforms import Form
from wtforms import StringField
from wtforms.validators import Regexp,InputRequired
import hashlib

class BaseForm(Form):
    def get_error(self):
        message = self.errors.popitem()[1][0]
        return message

    def validate(self):
        return super(BaseForm, self).validate()


class SmsCaptchaForm(BaseForm):
    salt = 'fgeWdLwg436t@$%$^'
    telephone = StringField(validators=[Regexp(r'1[345789]\d{9}')])
    # 这里的时间错是毫秒，验证13位就行了，14位已经是几百年后了
    timestamp = StringField(validators=[Regexp(r'\d{13}')])
    #签名必须输入就行
    sign = StringField(validators=[InputRequired()])

    def validate(self):
        #首先必须通过上面的验证，否则不在继续往下执行了
        result = super(SmsCaptchaForm, self).validate()
        if not result:
            return False

        telephone = self.telephone.data
        timestamp = self.timestamp.data
        sign = self.sign.data

        # md5(timestamp+telphone+salt)
        # md5函数必须要传一个bytes类型的字符串进去
        sign2 = hashlib.md5((timestamp + telephone + self.salt).encode('utf-8')).hexdigest()
        print('前端传来的sign',self.sign.data)
        print('后端计算的sign',sign2)
        if sign == sign2:
            return True
        else:
            return False