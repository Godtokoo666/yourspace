# app/routes.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, g
from app.services.user_service import UserService
from app.services.post_service import PostService
from .form import RegistrationForm, PostForm, CommentForm, confirmForm, SpaceForm

main = Blueprint('main', __name__)

@main.route('/')
def index():
    pagination=PostService.get_multi_by_create(1)
    posts=pagination.items
    return render_template('index.html',title='首页',posts=posts,pagination=pagination)

@main.route('/page-<int:page>')
def index_page(page):
    pagination=PostService.get_multi_by_create(page)
    if page>pagination.pages:
        return index_page(pagination.pages)
    elif page<1:
        return index_page(1)
    posts=pagination.items
    return render_template('index.html',title='首页',posts=posts,pagination=pagination)

@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usernameORemail = request.form['usernameORemail']
        if '@' in usernameORemail:
            user = UserService.get_by_email(usernameORemail)
        else:
            user = UserService.get_by_username(usernameORemail)
        password = request.form['password']
        if user and UserService.check_password(user.uid, password):
            session['user_id']=user.uid
            return redirect(url_for('main.index'))
        else:
            flash('用户名或邮箱或密码错误', 'error')
    return render_template('login.html', title='登录')

@main.route('/logout')
def logout():
    session['user_id']=None
    return redirect(url_for('main.index'))

@main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        UserService.add_user(form.username.data, form.password.data, form.email.data, 1, 1)
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('main.login'))
    return render_template('register.html', title='注册',form=form)

@main.route('/space/<int:uid>')
def space(uid):
    space=UserService.get_one(uid)    
    return render_template('space.html', title='个人空间', space=space)

@main.route('/space/<int:uid>/setting', methods=['GET', 'POST'])
def space_setting(uid):
    if g.user.uid != uid:
        return render_template('401.html', title='无权访问')
    user=UserService.get_one(uid)
    form=SpaceForm(obj=user)
    if request.method == 'POST':
        if form.validate_on_submit():
            UserService.update_profile(uid, form.avatar.data, form.bio.data)
            return redirect(url_for('main.space', uid=uid))
    return render_template('space_setting.html', title='设置', form=form)


@main.route('/node')
def node():
    if g.user.has_priv('PRIV_USER'):
        return render_template('node.html', title='节点')
    else:
        return redirect(url_for('main.login'))

@main.route('/post/<int:pid>', methods=['GET', 'POST'])
def post_detial(pid):
    post = PostService.get_one(pid)
    if g.user.level < post.access_level:
        render_template('401.html', title='无权访问')
    form= CommentForm()
    PostService.add_views(pid)
    comments=PostService.get_comments(pid)
    title = post.title
    if request.method == 'POST':
        if form.validate_on_submit():
            PostService.add_comment( form.content.data, g.user.uid, pid)
            return redirect(url_for('main.post_detial', pid=pid))
        print(comments)
    return render_template('post_detial.html', title=title, post=post, comments=comments, form=form)

@main.route('/post/create', methods=['GET', 'POST'])
def post_create():
    if not g.user.has_priv('PRIV_USER'):
        return redirect(url_for('main.login'))
    form = PostForm()
    if form.validate_on_submit():
        user_id = g.user.uid
        post=PostService.add_post(form.title.data, form.content.data, user_id, form.node.data)
        return redirect(url_for('main.post_detial', pid=post.pid))
    return render_template('post_create.html', title='创建讨论', form=form)


@main.route('/post/<int:pid>/edit', methods=['GET', 'POST'])
def post_edit(pid):
    post=PostService.get_one(pid)
    if g.user.uid != post.author and not g.user.has_priv('PRIV_ADMIN'):
        return render_template('401.html', title='无权访问')
    form = PostForm(obj=post)
    if request.method == 'POST':
        if form.validate_on_submit():
            PostService.update_post(pid, form.title.data, form.content.data, form.node.data)
            return redirect(url_for('main.post_detial', pid=pid))
    return render_template('post_edit.html', title='编辑主题', form=form,post=post)

@main.route('/post/<int:pid>/delete', methods=['GET', 'POST'])
def post_delete(pid):
    post=PostService.get_one(pid)
    if not g.user.has_priv('PRIV_ADMIN'):
        return render_template('401.html', title='无权访问')
    form=confirmForm()
    if form.validate_on_submit() and request.method == 'POST':
        print('delete post')
        PostService.delete_post(pid)
        return redirect(url_for('main.index'))
    message='您正在删除主题：「'+post.title+'」，请做最后确认！'
    return render_template('action_confirm.html', title='操作确认',message=message,action='/post/'+str(pid)+'/delete',form=form)

@main.route('/comment/<int:cid>/edit', methods=['GET', 'POST'])
def comment_edit(cid):
    comment=PostService.get_comment(cid)
    if g.user.uid != comment.author and not g.user.has_priv('PRIV_ADMIN'):
        return render_template('401.html', title='无权访问')
    form = CommentForm(obj=comment)
    if request.method == 'POST':
        if form.validate_on_submit():
            PostService.update_comment(cid, form.content.data)
            return redirect(url_for('main.post_detial', pid=comment.post))
    return render_template('comment_edit.html', title='编辑评论', form=form,comment=comment)

@main.route('/node/<string:node>')
def node_detail():
    
    return render_template('node.html', title='节点讨论')

@main.route('/admin')
def admin():
    return render_template('admin.html', title='管理后台')




