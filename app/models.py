from . import db
from .constants import privileges
from datetime import datetime


class User(db.Model):
    __tablename__ = 'Users'
    
    uid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    avatar = db.Column(db.String, default='/static/images/default_avatar.jpg')
    bio= db.Column(db.Text)
    level = db.Column(db.Integer, default=0)
    priv = db.Column(db.Integer, default=0)
    point = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.now,index=True)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    
    def __init__(self):
        self.priv = privileges['PRIV_GUEST']
        self.level = 0
        self.username = 'Guest'
    
    def __repr__(self):
        return '<User %r>' % self.username
    
    def has_priv(self, priv):
        return self.priv & self.priv == privileges[priv]

class Group(db.Model):
    __tablename__ = 'Groups'
    
    gid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False,index=True)
    description = db.Column(db.Text, nullable=False)
    priv = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    
    def add_group(self, name, description, priv):
        self.name = name
        self.description = description
        self.priv = priv
        db.session.add(self)
        db.session.commit()
        
    def update_group(self, name, description, priv):
        self.name = name
        self.description = description
        self.priv = priv
        db.session.commit()
        
    def delete_group(self):
        db.session.delete(self)
        db.session.commit()
        
    def __repr__(self):
        return '<Group %r>' % self.name
    
class UserGroup(db.Model):
    __tablename__ = 'UserGroups'
    
    uid = db.Column(db.Integer, db.ForeignKey('Users.uid'), primary_key=True)
    gid = db.Column(db.Integer, db.ForeignKey('Groups.gid'), primary_key=True)
    
    def add_user_group(self, uid, gid):
        self.uid = uid
        self.gid = gid
        db.session.add(self)
        db.session.commit()
    
    def __repr__(self):
        return '<UserGroup %r>' % self.uid
    
class Node(db.Model):
    __tablename__ = 'Nodes'
    
    nid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    description = db.Column(db.Text, nullable=False)
    parent = db.Column(db.Integer, db.ForeignKey('Nodes.nid'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    
    def __repr__(self):
        return '<Node %r>' % self.name
    
class Post(db.Model):
    __tablename__ = 'Posts'
    
    pid = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False, index=True)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.Integer, db.ForeignKey('Users.uid'), nullable=False)
    node = db.Column(db.Integer, db.ForeignKey('Nodes.nid'), nullable=False)
    access_level = db.Column(db.Integer, default=0)
    edited = db.Column(db.Boolean, default=False)
    topped = db.Column(db.Boolean, default=False)
    readonly = db.Column(db.Boolean, default=False)
    sort = db.Column(db.Integer, default=0)
    views = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.now, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.now)
    
    def __repr__(self):
        return '<Post %r>' % self.title
    
class Comment(db.Model):
    __tablename__ = 'Comments'
    
    cid = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.Integer, db.ForeignKey('Users.uid'), nullable=False)
    post = db.Column(db.Integer, db.ForeignKey('Posts.pid'), nullable=False)
    edited = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    
    def __repr__(self):
        return '<Comment %r>' % self.cid