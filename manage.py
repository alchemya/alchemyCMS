__author__ = 'yuchen'
__date__ = '2018/8/27 17:58'

from flask_script import Manager
from flask_migrate import MigrateCommand,Migrate
from LandiCMS import create_app
from exts import db
from apps.cms import models as cms_models
from apps.cms.models import CMSRole,CMSPermission,CMSUser
from apps.front.models import FrontUser,BoardModel,BannerModel,PostModel

app=create_app()
manage=Manager(app)
Migrate(app,db)
manage.add_command('db',MigrateCommand)

@manage.option('-u','--username',dest='username')
@manage.option('-p','--password',dest='password')
@manage.option('-e','--email',dest='email')
def create_cms_user(username,password,email):
    user=cms_models.CMSUser(username=username,password=password,email=email)
    db.session.add(user)
    db.session.commit()
    print('cms用户添加成功')



@manage.command
def create_role():
    #访问者(可以修改个人信息)
    visitor = CMSRole(name='访问者',desc='可以修改个人信息')
    visitor.permissions = CMSPermission.VISITOR

    #运营角色(修改个人信息，管理帖子，管理评论，管理前台用户)
    operator = CMSRole(name='运营', desc='管理帖子，评论，前台用户')
    operator.permissions = (CMSPermission.VISITOR|
                            CMSPermission.POSTER|
                            CMSPermission.COMMENTER|
                            CMSPermission.FRONTUSER)
    #管理员(拥有绝大部分权限)
    admin = CMSRole(name='管理员', desc='拥有本系统所有权限')
    admin.permissions = (CMSPermission.VISITOR|
                         CMSPermission.POSTER|
                         CMSPermission.COMMENTER|
                         CMSPermission.BOARDER|
                         CMSPermission.FRONTUSER|
                         CMSPermission.CMSUSER)
    #开发者
    developer = CMSRole(name='开发者', desc='开发人员专用')
    developer.permissions = CMSPermission.ALL_PERMISSION

    db.session.add_all([visitor, operator, admin, developer])
    db.session.commit()


@manage.option('-e', '--email', dest='email')
@manage.option('-r', '--role', dest='role')
def add_user_to_role(email, role):
    user = CMSUser.query.filter_by(email=email).first()
    if user:
        role_type = CMSRole.query.filter_by(name=role).first()
        if role_type:
            role_type.users.append(user)
            db.session.commit()
            print('用户{}添加到角色{}成功'.format(email, role))
        else:
            print('没有这个角色：{}'.format(role))
    else:
        print('没有这个用户：{}'.format(email))

@manage.command
def test_permission():
    user = CMSUser.query.first()  #目前我数据库只有一个账号
    if user.is_developer:
        print('用户{}有开发者的权限'.format(user.email))
    else:
        print('用户{}没有开发权限'.format(user.email))


#判断某个用户是否拥有某个角色的权限
@manage.option('-e','--email',dest='email')
@manage.option('-p','--permission_name',dest='permission_name')
def try_has_permission(email,permission_name):
    user=CMSUser.query.filter(CMSUser.email==email).first()
    if user:
        role_type=CMSRole.query.filter(CMSRole.name==permission_name).first()
        if role_type:
           if user.has_permission(role_type.permissions):
               print('{}有{}的权限'.format(email,permission_name))
           else:
               print('{}没有{}的权限'.format(email,permission_name))
        else:
            print('没有{}这个权限角色'.format(permission_name))
    else:
        print('没有{}这个用户'.format(email))


@manage.option('-t', '--telephone', dest='telephone')
@manage.option('-u', '--username', dest='username')
@manage.option('-p', '--password', dest='password')
def create_front_user(telephone, username, password):
    user = FrontUser(telephone=telephone, username=username, password=password)
    db.session.add(user)
    db.session.commit()
    print( '成功创建前台用户：{}'.format(username))

@manage.command
def create_test_post():
    for x in range(1,205):
        title='标题%s'%x
        content='内容%s' %x
        board=BoardModel.query.first()
        author=FrontUser.query.first()
        post=PostModel(title=title,content=content)
        post.board=board
        post.author=author
        db.session.add(post)
        db.session.commit()
    print('添加测试帖子成功了')



if __name__ == '__main__':
    manage.run()


