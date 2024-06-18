from ..models import db, Post, User, Comment
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
    def delete_post(cls, pid):
        post = Post.query.filter_by(pid=pid).first()
        db.session.delete(post)
        db.session.commit()
        return post
    
    @classmethod
    def get_comments(cls, pid):
        comments_query = db.session.query(
            Comment.cid,
            Comment.content,
            Comment.author,
            Comment.post,
            Comment.edited,
            Comment.created_at,
            Comment.updated_at,
            User.username,
            User.avatar
            ).join(User, Comment.author == User.uid)
        comments = comments_query.filter(Comment.post == pid).all()     
        return comments
    
    @classmethod
    def get_comment(cls, cid):
        comment=Comment.query.filter_by(cid=cid).first()
        return comment
    
    @classmethod
    def add_comment(cls, content, author, post):
        comment = Comment()
        comment.content = content
        comment.author = author
        comment.post = post
        db.session.add(comment)
        db.session.commit()
        return comment
    
    @classmethod
    def update_comment(cls, cid, content):
        comment = Comment.query.filter_by(cid=cid).first()
        comment.content = content
        comment.edited = True
        comment.updated_at = datetime.now()
        db.session.commit()
        return comment
    