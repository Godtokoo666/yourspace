from app.models import db, Comment, User, Post
from datetime import datetime

class CommentService:
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
        p = Post.query.filter_by(pid=post).first()
        p.commented_at = datetime.now()
        p.comment_count += 1
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
    