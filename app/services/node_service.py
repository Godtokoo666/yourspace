from app.models import db, Node

class NodeService:
    @classmethod
    def get_one(cls, nid):
        return Node.query.filter_by(nid=nid).first()
    
    @classmethod
    def get_multi(cls):
        return Node.query.all()
    
    @classmethod
    def get_multi_by_parent(cls, parent):
        return Node.query.filter_by(parent=parent).all()
    
    @classmethod
    def get_by_url(cls, url):
        return Node.query.filter_by(url=url).first()
    
    @classmethod
    def add_node(cls, name, description,url,avatar,access_level,parent):
        node = Node()
        node.name = name
        node.description = description
        node.url = url
        node.avatar=avatar
        node.access_level = access_level
        node.parent = parent
        db.session.add(node)
        db.session.commit()
        return node
    
    @classmethod
    def update_node(cls, nid, **kwargs):
        node = Node.query.filter_by(nid=nid).first()
        if node:
            if 'name' in kwargs:
                node.name = kwargs['name']
            if 'description' in kwargs:
                node.description = kwargs['description']
            if 'url' in kwargs:
                node.url = kwargs['url']
            if 'avatar' in kwargs:
                node.avatar = kwargs['avatar']
            if 'access_level' in kwargs:
                node.access_level = kwargs['access_level']
            if 'parent' in kwargs:
                node.parent = kwargs['parent']
            db.session.commit()
        return node
    
    @classmethod
    def delete_node(cls, nid):
        node = Node.query.filter_by(nid=nid).first()
        if node:
            db.session.delete(node)
            db.session.commit()
        return node