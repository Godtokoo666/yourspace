from app.models import db, Group

class GroupService:
    
    @classmethod
    def get_one(cls, gid):
        return Group.query.filter_by(gid=gid).first()
    
    @classmethod
    def get_multi(cls):
        return Group.query.all()
    
    @classmethod
    def add_group(cls, groupname):
        group = Group()
        group.add_group(groupname)
        return group
    
    @classmethod
    def update_group(cls, gid, groupname):
        group = Group.query.filter_by(gid=gid).first()
        group.update_group(groupname)
        return group
    
    @classmethod
    def delete_group(cls, gid):
        group = Group.query.filter_by(gid=gid).first()
        group.delete_group()
        return group
 