from app.models import db, User
from werkzeug.security import generate_password_hash, check_password_hash

class UserService:
    
    @classmethod
    def get_by_username(cls,username):
        return User.query.filter_by(username=username).first()
    
    @classmethod
    def get_by_email(cls,email):
        return User.query.filter_by(email=email).first()
    
    @classmethod
    def get_one(cls,uid):
        return User.query.filter_by(uid=uid).first()
    
    @classmethod
    def get_muilt(cls):
        return User.query.all()
    
    @classmethod
    def add_user(cls,username,password,email,priv,level):
        user=User()
        user.username=username
        user.password=generate_password_hash(password)
        user.email=email
        user.priv=priv
        user.level=level
        db.session.add(user)
        db.session.commit()
        return user
    
    @classmethod
    def update_profile(cls,uid,avatar,bio):
        user=User.query.filter_by(uid=uid).first()
        if user:
            user.avatar=avatar
            user.bio=bio
            db.session.commit()
        return user
    
    @classmethod
    def update_user(cls,uid, **kwargs):
        user=User.query.filter_by(uid=uid).first()
        if user:
            if 'username' in kwargs:
                user.username = kwargs['username']
            if 'password' in kwargs:
                user.password = generate_password_hash(kwargs['password'])
            if 'email' in kwargs:
                user.email = kwargs['email']
            if 'priv' in kwargs:
                user.priv = kwargs['priv']
            if 'level' in kwargs:
                user.level = kwargs['level']
            if 'banned' in kwargs:
                user.banned = kwargs['banned']
            db.session.commit()
        return user
    
    @classmethod
    def delete_user(cls,uid):
        user=User.query.filter_by(uid=uid).first()
        db.session.delete(user)
        return user
    
    @classmethod
    def check_password(cls,uid,password):
        user=User.query.filter_by(uid=uid).first()
        if user:
            return check_password_hash(user.password, password)
        return False
    
    @classmethod
    def has_priv(cls,uid,priv):
        user=User.query.filter_by(uid=uid).first()
        return user.priv >= priv