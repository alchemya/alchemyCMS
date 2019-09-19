__author__ = 'yuchen'
__date__ = '2018/8/27 17:38'

from flask import Blueprint,render_template,views,request,session,redirect,url_for,g,jsonify
from .forms import LoginForm,ResetpwdForm,RestEmailForm,AddBannerForm,UpdateBannerForm,AddBoardsForm,UpdateBoardForm
from .models import CMSUser,CMSPermission
from sqlalchemy import and_
from datetime import timedelta
from .decorators import login_required,permission_required
from config import CMS_USER_ID
from exts import db,Mail
from utils import resful
from flask_mail import Message
from exts import mail
import string
import random
from utils import landicache
from apps.front.models import BannerModel,BoardModel,HighLight,PostModel,CommentModel,FrontUser
import qiniu
from flask_paginate import Pagination,get_page_parameter




bp=Blueprint('cms',__name__,url_prefix='/cms')


@bp.route('/')
@login_required
def index():
    return render_template('cms/cms_index.html')

@bp.route('/logout/')
@login_required
def logout():
    del session[CMS_USER_ID]
    return redirect(url_for('cms.login'))

@bp.route('/profile/')
@login_required
@permission_required(CMSPermission.VISITOR)
def profile():
    return render_template('cms/cms_profile.html')


@bp.route('/test_email/')
def test_email():
    msg = Message('Flask项目测试邮件',  #这是邮件主题
                  sender='1005862748@qq.com',
                  recipients=['568019867@qq.com'], #发送给谁，这是个列表，可以有多个接收者
                  body='Hello, 这是一封测试邮件，这是邮件的正文')
    mail.send(msg) #发送
    return 'success'

#登陆
class LoginView(views.MethodView):
    def get(self,message=None):
        return render_template('cms/cms_login.html',message=message)
    def post(self):
        form=LoginForm(request.form)
        if form.validate():
            email=form.email.data
            password=form.password.data
            remember=form.remember.data
            user=CMSUser.query.filter(CMSUser.email==email).first()
            if user and user.check_password(password):
                session[CMS_USER_ID]=user.id
                if remember:
                    session.permanent=True
                return redirect(url_for('cms.index'))
            else:
                return self.get(message='邮箱或者密码错误')
        else:
            print(form.errors)
            # message=form.errors.popitem()[1][0]
            message=form.get_error()
            return self.get(message=message)

#修改密码
class ResetPwdView(views.MethodView):
    decorators = [login_required]
    def get(self):
        print(g.cms_user._password,'好')
        return render_template('cms/cms_resetpwd.html')
    def post(self):
        form=ResetpwdForm(request.form)
        print(form.data)
        if form.validate():
            oldpassword=form.oldpwd.data
            newpassword=form.newpwd.data

            user=g.cms_user
            if user.check_password(oldpassword):
                user.password=newpassword
                db.session.commit()
                return resful.success('密码修改成功')
            else:
                return resful.params_error('旧密码输入错误')
        else:
            message=form.get_error()
            return resful.params_error(message)


#修改邮箱
class ResetEmailView(views.MethodView):
    decorators = [login_required]
    def get(self):
        return render_template('cms/cms_resetemail.html')

    def post(self):
        reset_email_form=RestEmailForm(request.form)
        if reset_email_form.validate():
            email=reset_email_form.email.data
            g.cms_user.email=email
            db.session.commit()
            return resful.success('修改成功')
        elif reset_email_form.errors:
            print(reset_email_form.errors)
            errors=reset_email_form.get_error()
            return resful.params_error(errors)
        else:
            return resful.server_error()










bp.add_url_rule('/login/',view_func=LoginView.as_view('login'))
bp.add_url_rule('/resetpwd/',view_func=ResetPwdView.as_view('resetpwd'))
bp.add_url_rule('/resetemail/', view_func=ResetEmailView.as_view('resetemail'))


#发送邮箱验证码
@bp.route('/email_captcha/')
def email_captcha():
    email=request.args.get('email')
    if not email:
        return resful.params_error('请输入你的邮箱')
    source=list(string.ascii_letters)
    source.extend(map(lambda x:str(x),range(0,10)))
    #还有一种写法,但是太low了
    # source.extend(['0','1','2','3','4','5','6','7','8','9','10'])
    random_code_captcha=random.sample(source,6)
    captcha=''.join(random_code_captcha)
    message=Message('论坛邮箱验证码',recipients=[email],body='您的验证码是%s'%captcha)
    try:
        mail.send(message)
    except:
        return resful.server_error()

    landicache.set(email,captcha)

    return resful.success('邮件已发送')


@bp.route('/comments/')
@login_required
@permission_required(CMSPermission.COMMENTER)
def comments():
    comments=CommentModel.query.order_by(CommentModel.create_time.desc()).all()
    return render_template('cms/cms_comments.html',comments=comments)


@bp.route('/fusers/')
@login_required
@permission_required(CMSPermission.FRONTUSER)
def fusers():
    users=FrontUser.query.order_by(FrontUser.join_time.desc()).all()
    return render_template('cms/cms_fusers.html',users=users)

@bp.route('/cusers/')
@login_required
@permission_required(CMSPermission.CMSUSER)
def cusers():
    return render_template('cms/cms_cusers.html')


@bp.route('/croles/')
@login_required
@permission_required(CMSPermission.ALL_PERMISSION)
def croles():
    return render_template('cms/cms_croles.html')
    


@bp.route('/banners/')
@login_required
@permission_required(CMSPermission.COMMENTER)
def banners():
    banners=BannerModel.query.order_by(BannerModel.priority.desc()).all()
    return render_template('cms/cms_banners.html',banners=banners)

@bp.route('/add_banners/',methods=['POST'])
@login_required
def add_banners():
    form=AddBannerForm(request.form)
    if form.validate():
        # name1=request.form.get('name')
        name=form.name.data
        # print(name1,name,'美丽的世界')
        image_url=form.image_url.data
        link_url=form.link_url.data
        priority=form.priority.data
        banner=BannerModel(name=name,image_url=image_url,link_url=link_url,priority=priority)
        db.session.add(banner)
        db.session.commit()
        return resful.success()
    else:
        print(form.errors)
        return resful.params_error(form.get_error())


@bp.route('/update_banners/',methods=['POST','GET'])
@login_required
def update_banners():
    form=UpdateBannerForm(request.form)
    print(form.data,'llal')
    if form.validate():
        banner_id=form.banner_id.data
        name=form.name.data
        image_url=form.image_url.data
        link_url=form.link_url.data
        priority=form.priority.data
        banner=BannerModel.query.get_or_404(banner_id)
        if banner:
            banner.name=name
            banner.image_url=image_url
            banner.link_url=link_url
            banner.priority=priority
            db.session.add(banner)
            db.session.commit()
            return resful.success()
        else:
            return resful.params_error(message='没有这个轮播图')
    else:
        return resful.params_error(message=form.get_error())

@bp.route('/delete_banner/',methods=['POST'])
@login_required
def delete_banner():
    banner_id=request.form.get('banner_id')
    print(banner_id)
    if not banner_id:
        return resful.params_error(message='请传入轮播图id')
    banner=BannerModel.query.get(banner_id)
    if not banner:
        return resful.params_error(message='没有这个轮播图')
    db.session.delete(banner)
    db.session.commit()
    return resful.success()


@bp.route('/uptoken/')
def uptoken():
    access_key='7wL2HnNizlF2OCeFGkmu2KdMG0exOXsA5GQi8EMT'
    secrect_key='fYQ30QziTfynz-osSuoq6pA7xewupEy764l6Zxgl'
    q=qiniu.Auth(access_key,secrect_key)
    bucket='images'
    token=q.upload_token(bucket)
    return jsonify({'uptoken':token})


@bp.route('/boards/')
@login_required
@permission_required(CMSPermission.BOARDER)
def boards():
    board_models=BoardModel.query.all()
    context={
        'boards':board_models
    }
    return render_template('cms/cms_boards.html',**context)

@bp.route('/add_boards/',methods=['POST'])
@login_required
@permission_required(CMSPermission.BOARDER)
def add_boards():
    form=AddBoardsForm(request.form)
    if form.validate():
        name=form.name.data
        board=BoardModel(name=name)
        db.session.add(board)
        db.session.commit()
        return resful.success()
    else:
        return resful.params_error(message=form.get_error())


@bp.route('/update_boards/',methods=['POST'])
@login_required
@permission_required(CMSPermission.BOARDER)
def update_boards():
    form=UpdateBoardForm(request.form)
    if form.validate():
        board_id=form.board_id.data
        name=form.name.data
        board=BoardModel.query.get(board_id)
        if board:
            board.name=name
            db.session.commit()
            return resful.success()
        else:
            return resful.params_error(message='没有这个版块')
    else:
        return resful.params_error(message=form.get_error())


@bp.route('/delete_boards/',methods=['POST'])
@login_required
@permission_required(CMSPermission.BOARDER)
def delete_boards():
    board_id=request.form.get('board_id')
    if not board_id:
        return resful.params_error(message='请传入版块ID')
    board=BoardModel.query.get(board_id)
    if board:
        db.session.delete(board)
        db.session.commit()
        return resful.success()
    else:
        return resful.params_error(message='没有这个版块')

# @bp.route('/delete_post/',methods=['POST'])
# @login_required
# @permission_required(CMSPermission.BOARDER)
# def delete_post():
#     post_id=request.form.get('')

@bp.route('/posts/')
@login_required
@permission_required(CMSPermission.POSTER)
def posts():
    page = request.args.get(get_page_parameter(), type=int, default=1)
    start = (page - 1) * 10
    end = start + 10
    posts = PostModel.query.order_by(PostModel.create_time.desc()).slice(start, end)
    total = PostModel.query.count()
    print(page,"and和",total)
    pagination = Pagination(bs_version=3, page=page, total=total, outer_window=1, inner_window=2)
    print(pagination.links)
    context = {
        'posts': posts,
        'pagination':pagination
    }

    return render_template('cms/cms_posts.html', **context)


@bp.route('/hpost/',methods=['POST'])
@login_required
@permission_required(CMSPermission.POSTER)
def hpost():
    post_id=request.form.get('post_id')
    if not post_id:
        return resful.params_error(message='请传入帖子id')
    post=PostModel.query.get(post_id)
    if not post:
        return resful.params_error(message='没有这篇帖子')
    highlight=HighLight()
    highlight.post=post
    db.session.add(highlight)
    db.session.commit()
    return resful.success()



@bp.route('/uhpost/',methods=['POST'])
@login_required
@permission_required(CMSPermission.POSTER)
def uhpost():
    post_id = request.form.get('post_id')
    if not post_id:
        return resful.params_error(message='请传入帖子id')
    post = PostModel.query.get(post_id)
    if not post:
        return resful.params_error(message='没有这篇帖子')
    # print(post_id,'ddd')
    highlight=HighLight.query.filter_by(post_id=post_id).first()
    # print(highlight)
    db.session.delete(highlight)
    db.session.commit()
    return resful.success()

