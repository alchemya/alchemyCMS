__author__ = 'yuchen'
__date__ = '2018/8/29 11:04'

z,y=lambda x:str(x),range(0,9)

k=map(z,y)
print(list(k))
import os

# import memcache
#
# mc=memcache.Client(["127.0.0.1:11211"],debug=True)
# # user=mc.get('boy')
# # print(user)
# mc.set_multi({'user':'yawen','shabi':'yuchen'},time=69)

# mc.set('yawen','meili',60)
# mc.decr('age',delta=4)
# from yunpian_python_sdk.model import constant as YC
# from yunpian_python_sdk.ypclient import YunpianClient
# # 初始化client,apikey作为所有请求的默认值
# clnt = YunpianClient('ddad7d6a0a582ae5a022f93b1c355494')
# param = {YC.MOBILE:'15658156691',YC.TEXT:'【雨晨生鲜食品】刘仲敬的验证码是1234。如非本人操作，请忽略本短信'}
# r = clnt.sms().single_send(param)


# path1 = os.path.dirname(__file__)
# print(path1)
# path2 = os.path.dirname(os.path.dirname(__file__)) #
# print(path2)
# code='ddsd'
# message='【雨晨论坛】您的验证码是{}。如非本人操作，请忽略本短信'.format(code)
# print(message)

# import hashlib
#
# # 待加密信息
# str = 'this is a md5 test.'
#
# # 创建md5对象
# hl = hashlib.md5()
# hx = hashlib.md5(str.encode('utf8')).hexdigest()
#
# # Tips
# # 此处必须声明encode
# # 若写法为hl.update(str)  报错为： Unicode-objects must be encoded before hashing
# hl.update(str.encode(encoding='utf-8'))
#
# print('MD5加密前为 ：' + str)
# print('MD5加密后为 ：' + hl.hexdigest())
# print('换一种的MD5加密后为 ：' +hx)

print('L4Kd3'.lower())
print(type(1))