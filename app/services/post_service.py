from app.models import db, Post, User, Node
from flask import request
from datetime import datetime

class PostService:
    @classmethod
    def get_one(cls, pid):
        post_query = db.session.query(
            Post.pid,
            Post.title,
            Post.node,
            Post.edited,
            Post.content,
            Post.access_level,
            Post.topped,
            Post.readonly,
            Post.views,
            Post.author,
            Post.created_at,
            Post.updated_at,
            User.username,
            User.avatar
            ).join(User, Post.author == User.uid)
        return post_query.filter(Post.pid==pid).first()
    
    
    @classmethod
    def get_multi_by_create(cls,page,node=None):
        # page = request.args.get(page, type=int, default=1)
        per_page = 20
        posts_query = db.session.query(
            Post.pid,
            Post.title,
            Post.node,
            Post.content,
            Post.access_level,
            Post.edited,
            Post.topped,
            Post.readonly,
            Post.sort,
            Post.created_at,
            Post.updated_at,
            Post.views,
            Post.author,
            User.username,
            User.avatar
            ).join(User, Post.author == User.uid).order_by(Post.created_at.desc())
        if node:
            posts_query = posts_query.filter(Post.node==node)
        posts_pagination = posts_query.paginate(page=page, per_page=per_page,error_out=False)
        if posts_pagination.pages>10:
            posts_pagination.it_pages = 10
        return posts_pagination
    
    @classmethod
    def get_multi_by_reply(cls):
        page = request.args.get('page', type=int, default=1)
        per_page = 10
        posts = Post.query.paginate(page, per_page, False)
        return posts
    
    @classmethod
    def get_multi_by_node(cls, node):
        page = request.args.get('page', type=int, default=1)
        per_page = 10
        posts = Post.query.filter_by(node=node).paginate(page, per_page, False)
        return posts
    
    
    @classmethod
    def add_post(cls, title, content, author, node):
        post = Post()
        post.title = title
        post.content = content
        post.author = author
        post.node = node
        db.session.add(post)
        n = Node.query.filter_by(nid=node).first()
        n.post_count += 1
        db.session.commit()
        return post
    
    @classmethod
    def add_views(cls, pid):
        post = Post.query.filter_by(pid=pid).first()
        post.views += 1
        db.session.commit()
        return post
    
    @classmethod
    def update_post(cls, pid, title, content, node):
        post = Post.query.filter_by(pid=pid).first()
        post.title = title
        post.content = content
        post.node = node
        post.updated_at = datetime.now()
        post.edited = True
        db.session.commit()
        return post
    
    @classmethod
    def update_by_admin(cls, pid, **kwargs):
        post = Post.query.filter_by(pid=pid).first()
        if post:
            if 'node' in kwargs:
                post.node = kwargs['node']
            if 'access_level' in kwargs:
                post.access_level = kwargs['access_level']
            if 'topped' in kwargs:
                post.topped = kwargs['topped']
            if 'readonly' in kwargs:
                post.readonly = kwargs['readonly']
            if 'sort' in kwargs:
                post.sort = kwargs['sort']
            db.session.commit()
        return post
    @classmethod
    def delete_post(cls, pid):
        post = Post.query.filter_by(pid=pid).first()
        db.session.delete(post)
        db.session.commit()
        return post
    