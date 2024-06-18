from ..app.models import User, Group, privileges, db


group=Group()
group.name='Default'
group.description='Default group'
group.priv=privileges['PRIV_USER']
db.session.add(group)
db.session.commit()
