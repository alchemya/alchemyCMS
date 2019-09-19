__author__ = 'yuchen'
__date__ = '2018/8/27 17:38'

from flask import (
    Blueprint,
    views,
    render_template,
    make_response,
    request,
    session,
    redirect,
    url_for,
    g,
    abort
)
from config import FRONT_USER_ID
from io import BytesIO
from utils.captcha import Captcha
from .forms import SignUpForm,LoginForm,AddPostForm,AddCommentForm,IForgetForm
from .models import FrontUser
from exts import db
from utils import resful,safeutils
from apps.front.models import BannerModel,BoardModel,PostModel,CommentModel,HighLight
from .decorators import login_requried
from flask_paginate import Pagination,get_page_parameter
from config import DevConfig



from sqlalchemy import func,or_

bp=Blueprint('front',__name__)



@bp.route('/')
def index():
    board_id=request.args.get('bd',type=int,default=None)
    page = request.args.get(get_page_parameter(), type=int, default=1)
    sort = request.args.get('st', type=int, default=1)

    banners = BannerModel.query.order_by(BannerModel.priority.desc()).limit(4)
    boards = BoardModel.query.all()

    start = (page-1)*DevConfig.PER_PAGE
    end=start+DevConfig.PER_PAGE
    posts=None
    total=0
    query_obj = None

    if sort == 1:
        query_obj = PostModel.query.order_by(PostModel.create_time.desc())
    elif sort == 2:
        query_obj = db.session.query(PostModel).outerjoin(HighLight).order_by(HighLight.create_time.desc(),
                                                                              PostModel.create_time.desc())
    elif sort == 3:
        query_obj = PostModel.query.order_by(PostModel.reading_count.desc())
    elif sort == 4:
        query_obj = db.session.query(PostModel).outerjoin(CommentModel).group_by(PostModel.id).order_by(
            func.count(CommentModel.id).desc(), PostModel.create_time.desc())


    if board_id:
        query_board=query_obj.filter(PostModel.board_id==board_id).order_by(PostModel.create_time.desc())
        posts=query_board.slice(start,end)
        total=query_board.count()
    else:
        posts=query_obj.slice(start,end)
        total=query_obj.count()
    pagination = Pagination(bs_version=3,page=page, total=total,outer_window=0,inner_window=3)
    context = {
        'banners': banners,
        'boards': boards,
        'posts': posts,
        'pagination':pagination,
        'current_board':board_id,
        'current_sort':sort
    }
    return render_template('front/front_index.html', **context)



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
    return resp


@bp.route('/login/',methods=['POST','GET'])
def login_in():
    if request.method =='GET':
        if session.get(FRONT_USER_ID):
            return redirect(url_for('front.index'))
        else:
            return_to=request.referrer
            if return_to and return_to!=request.url \
                    and return_to != url_for('front.signup') and safeutils.is_safe_url(return_to):
                return render_template('front/front_login.html',return_to=return_to)
            return render_template('front/front_login.html')
    else:
        form=LoginForm(request.form)
        # print(form.data)
        if form.validate():
            telephone=form.telephone.data
            password=form.password.data
            remember=form.remember.data
            user=FrontUser.query.filter_by(telephone=telephone).first()
            if user and user.check_password(password):
                session[FRONT_USER_ID]=user.id
                if remember:
                    session.permanent = True
                return resful.success()
            else:
                return resful.params_error('手机号或密码错误')
        else:
            return resful.params_error(form.get_error())

@bp.route('/logout/')
def log_out():
    del session[FRONT_USER_ID]
    return redirect(url_for('front.index'))

    

class SignUpViews(views.MethodView):
    def get(self):
        # 获取上一个页面的url
        return_to = request.referrer
        # referrer不一定会存在，比如直接访问的登录页面
        # 并且它不等于登录页面的url
        # 并且这个referre是个安全的url,防止恶意者去伪造它，被跳转到其它恶意的网站
        if return_to and return_to != request.url and safeutils.is_safe_url(return_to):
            # 把这个url传入到模板中
            return render_template('front/front_signup.html', return_to=return_to)
        return render_template('front/front_signup.html')

    def post(self):
        form=SignUpForm(request.form)
        print(form.data)
        if form.validate():
            telephone=form.telephone.data
            username=form.username.data
            password=form.password1.data
            user=FrontUser(telephone=telephone,password=password,username=username)
            db.session.add(user)
            db.session.commit()
            return resful.success()
        else:
            print(form.errors)
            return resful.params_error(form.get_error())

@bp.route('/i_forget/',methods=['POST','GET'])
def i_forget():
    if request.method == 'GET':
        return render_template('front/front_iforget.html')
    else:
        form = IForgetForm(request.form)
        if form.validate():
            user = FrontUser.query.filter_by(telephone=form.telephone.data).first()
            print(user)
            user.password = form.password1.data
            db.session.add(user)
            db.session.commit()
            session.clear()
            return resful.success('密码修改成功')
        else:
            print(form.errors)
            return resful.params_error(form.get_error())

bp.add_url_rule('/signup/', view_func=SignUpViews.as_view('signup'))

@bp.route('/add_post/',methods=['POST','GET'])
@login_requried
def add_post():
    if request.method == 'GET':
        boards = BoardModel.query.all()
        cboard=request.args.get('cboard',type=int,default=None)
        return render_template('front/front_add_post.html', boards=boards,cboard=cboard)
    else:

        form = AddPostForm(request.form)
        if form.validate():
            title = form.title.data
            content = form.content.data
            board_id = form.board_id.data
            board = BoardModel.query.get(board_id)
            if not board:
                return resful.params_error(message='没有这个版块')
            post = PostModel(title=title, content=content, board_id=board_id)
            post.board = board
            post.author = g.front_user
            db.session.add(post)
            db.session.commit()
            return resful.success('注册成功')
        else:
            return resful.params_error(message=form.get_error())


@bp.route('/p/<post_id>')
def post_detail(post_id):
    post=PostModel.query.get(post_id)
    post.reading_count+=1
    db.session.add(post)
    db.session.commit()
    if not post:
        abort(404)
    return render_template('front/front_postdetail.html',post=post)


@bp.route('/add_comment/',methods=['POST'])
@login_requried
def add_comment():
    form=AddCommentForm(request.form)

    if form.validate():
        content=form.content.data
        post_id=form.post_id.data
        post=PostModel.query.get(post_id)
        print(form.data)
        if post:
            comment=CommentModel(content=content)
            comment.post=post
            comment.author=g.front_user
            db.session.add(comment)
            db.session.commit()
            return resful.success()
        else:
            return resful.params_error(message='没有这个帖子')
    else:
        return resful.params_error(form.get_error())

@bp.route('/pwd/')
@login_requried
def pwd():
    return render_template('front/pwd.html')


@bp.route('/search/')
def search():
    q=request.args.get('q')
    posts=PostModel.query.filter(or_(PostModel.title.contains(q),
                                        PostModel.content.contains(q))).order_by(PostModel.create_time.desc()).all()
    boards = BoardModel.query.all()
    return render_template('front/front_search.html',posts=posts,boards=boards)






