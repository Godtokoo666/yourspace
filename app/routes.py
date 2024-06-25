# app/routes.py
from flask import Blueprint, render_template, request, redirect,abort, url_for, flash, session, g
import markdown
from app.services.user_service import UserService
from app.services.post_service import PostService
from app.services.comment_service import CommentService
from app.services.node_service import NodeService
from app.form import SiteForm, RegistrationForm, PostForm, CommentForm, confirmForm, SpaceForm, AdminUserForm, AdminNodeForm, AdminPostForm

main = Blueprint('main', __name__)


@main.app_template_filter('time_from_now')
def time_from_now(time):
    from datetime import datetime
    from babel.dates import format_timedelta
    return format_timedelta(datetime.now()-time, locale='zh_CN')

@main.app_template_filter('md_to_html')
def md_to_html(md):
    return markdown.markdown(md, extensions=['markdown.extensions.extra', 'markdown.extensions.codehilite','markdown.extensions.tables','markdown.extensions.toc'])

@main.route('/')
def index():
    n=NodeService.get_multi()
    nodes= {node.nid: (node.name, node.url) for node in n}
    pagination=PostService.get_multi_by_create(1)
    posts=pagination.items
    return render_template('index.html',title='首页',posts=posts,pagination=pagination,nodes=nodes)

@main.route('/page-<int:page>')
def index_page(page):
    n=NodeService.get_multi()
    pagination=PostService.get_multi_by_create(page)
    if page>pagination.pages:
        return index_page(pagination.pages)
    elif page<1:
        return index_page(1)
    posts=pagination.items
    nodes= {node.nid: (node.name, node.url) for node in n}
    return render_template('index.html',title='首页',posts=posts,pagination=pagination,nodes=nodes)

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
        UserService.add_user(form.username.data, form.password.data, form.email.data, 2, 1)
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('main.login'))
    return render_template('register.html', title='注册',form=form)

@main.route('/space/<int:uid>')
def space(uid):
    space=UserService.get_one(uid)
    if not space:
        return render_template('404.html', title='404')
    return render_template('space.html', title='个人空间', space=space)

@main.route('/space/<int:uid>/setting', methods=['GET', 'POST'])
def space_setting(uid):
    if g.user.uid != uid or g.user.check_ban_status('BANNED_SETTING'):
        return render_template('401.html', title='无权访问')
    user=UserService.get_one(uid)
    form=SpaceForm(obj=user)
    if request.method == 'POST':
        if form.validate_on_submit():
            UserService.update_profile(uid, form.avatar.data, form.bio.data)
            return redirect(url_for('main.space', uid=uid))
    return render_template('space_setting.html', title='设置', form=form)

@main.route('/post/<int:pid>', methods=['GET', 'POST'])
def post_detial(pid):
    post = PostService.get_one(pid)
    node = NodeService.get_one(post.node)
    if g.user.level < post.access_level or g.user.check_ban_status('BANNED_ALL'):
        return render_template('401.html', title='无权访问')
    form= CommentForm()
    if g.user.uid != None:
        PostService.add_views(pid)
    comments=CommentService.get_comments(pid)
    title = post.title
    if request.method == 'POST':
        if form.validate_on_submit():
            CommentService.add_comment( form.content.data, g.user.uid, pid)
            return redirect(url_for('main.post_detial', pid=pid))
    return render_template('post_detail.html', title=title, post=post, comments=comments, node=node, form=form)

@main.route('/post/create', methods=['GET', 'POST'])
def post_create():
    if not g.user.has_priv('PRIV_USER') or g.user.check_ban_status('BANNED_POST'):
        return redirect(url_for('main.login'))
    form = PostForm()
    nodes=NodeService.get_multi()
    form.node.choices = [(n.nid, n.name) for n in nodes]
    if form.validate_on_submit():
        user_id = g.user.uid
        post=PostService.add_post(form.title.data, form.content.data, user_id, form.node.data)
        return redirect(url_for('main.post_detial', pid=post.pid))
    return render_template('post_create.html', title='创建讨论', form=form)


@main.route('/post/<int:pid>/edit', methods=['GET', 'POST'])
def post_edit(pid):
    post=PostService.get_one(pid)
    if g.user.uid != post.author and not g.user.has_priv('PRIV_ADMIN') and g.user.check_ban_status('BANNED_POST'):
        return render_template('401.html', title='无权访问')
    form = PostForm(obj=post)
    nodes=NodeService.get_multi()
    form.node.choices = [(n.nid, n.name) for n in nodes]
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
    comment=CommentService.get_comment(cid)
    if g.user.uid != comment.author or not g.user.has_priv('PRIV_ADMIN') or g.user.check_ban_status('BANNED_COMMENT'):
        return render_template('401.html', title='无权访问')
    form = CommentForm(obj=comment)
    if request.method == 'POST':
        if form.validate_on_submit():
            CommentService.update_comment(cid, form.content.data)
            return redirect(url_for('main.post_detial', pid=comment.post))
    return render_template('comment_edit.html', title='编辑评论', form=form,comment=comment)

@main.route('/node')
def node():
    nodes=NodeService.get_multi()
    return render_template('node.html', title='节点',nodes=nodes)

@main.route('/node/<string:url>')
def node_detail(url):
    node=NodeService.get_by_url(url)
    pagination=PostService.get_multi_by_create(1,node.nid)
    posts=pagination.items
    return render_template('node_detail.html', title=node.name, node=node, posts=posts,pagination=pagination)

@main.route('/node/<string:url>/page-<int:page>')
def node_detail_page(url,page):
    node=NodeService.get_by_url(url)
    pagination=PostService.get_multi_by_create(page,node.nid)
    if page>pagination.pages:
        return index_page(pagination.pages)
    elif page<1:
        return index_page(1)
    posts=pagination.items
    return render_template('node_detail.html', title=node.name, node=node, posts=posts,pagination=pagination)
@main.route('/admin',methods=['GET', 'POST'])
def admin():
    if not g.user.has_priv('PRIV_ADMIN'):
        return render_template('401.html', title='无权访问')
    userform = AdminUserForm()
    nodeform = AdminNodeForm()
    postform = AdminPostForm()
    if request.method == 'POST':
        if userform.submit.data and userform.validate_on_submit():
            uids=userform.uid.data.split(' ')
            dic={}
            if userform.level.data!=None:
                dic['level']=userform.level.data
            if userform.priv.data!=None:
                dic['priv']=userform.priv.data
            if userform.banned_status.data!=None:
                dic['banned']=userform.banned_status.data
            for uid in uids:
                if not UserService.get_one(uid):
                    flash('UID'+uid+'不存在', 'user')
                    return redirect(url_for('main.admin')+'#user_control')
                UserService.update_user(uid=uid, **dic)
            flash('提交成功', 'user')
            return redirect(url_for('main.admin')+'#user_control')
        if postform.submit.data and postform.validate_on_submit():
            pids=postform.pid.data.split(' ')
            dic={}
            if postform.node.data!=None:
                if not NodeService.get_one(postform.node.data):
                    flash('NID'+str(postform.node.data)+'不存在', 'post')
                    return redirect(url_for('main.admin')+'#post_control')
                dic['node']=postform.node.data
            if postform.access_level.data!=None:
                dic['access_level']=postform.access_level.data
            if postform.sort.data!=None:
                dic['sort']=postform.sort.data
            dic['topped']=postform.topped.data
            dic['readonly']=postform.readonly.data
            for pid in pids:
                if not PostService.get_one(pid):
                    flash('PID'+pid+'不存在', 'post')
                    return redirect(url_for('main.admin')+'#post_control')
                PostService.update_by_admin(pid=pid, **dic)
            flash('提交成功', 'post')
            return redirect(url_for('main.admin')+'#post_control')
        if nodeform.submit.data and nodeform.validate_on_submit():
            nid=nodeform.nid.data
            if nid :
                dic={}
                if nodeform.name.data:
                    dic['name']=nodeform.name.data
                if nodeform.description.data:
                    dic['description']=nodeform.description.data
                if nodeform.access_level.data!=None:
                    dic['access_level']=nodeform.access_level.data
                if nodeform.url.data:
                    dic['url']=nodeform.url.data
                if nodeform.avatar.data:
                    dic['avatar']=nodeform.avatar.data
                if nodeform.parent.data:
                    if not NodeService.get_one(nodeform.parent.data):
                        flash('父节点NID'+str(nodeform.parent.data)+'不存在', 'node')
                        return redirect(url_for('main.admin')+'#node_control')
                    dic['parent']=nodeform.parent.data
                if not NodeService.get_one(nid):
                    flash('NID'+str(nid)+'不存在', 'node')
                    return redirect(url_for('main.admin')+'#node_control')
                NodeService.update_node(nid=nid, **dic)
                flash('节点更新成功', 'node')
                return redirect(url_for('main.admin')+'#node_control')
            else:
                if nodeform.parent.data == None or not nodeform.name.data or not nodeform.description.data or nodeform.access_level.data == None:
                    flash('添加失败，请填写完整信息', 'node')
                    return redirect(url_for('main.admin')+'#node_control')
                if not NodeService.get_one(nodeform.parent.data):
                    flash('父节点NID'+str(nodeform.parent.data)+'不存在', 'node')
                    return redirect(url_for('main.admin')+'#node_control')
                NodeService.add_node(nodeform.name.data, nodeform.description.data, nodeform.url.data, nodeform.avatar.data, nodeform.parent.data, nodeform.access_level.data)
                flash('节点添加成功', 'node')
                return redirect(url_for('main.admin')+'#node_control')
    return render_template('admin.html', title='管理后台', userform=userform, nodeform=nodeform, postform=postform)




