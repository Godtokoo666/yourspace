"""Initial migration

Revision ID: 2e8e3b7068c2
Revises: 
Create Date: 2024-06-25 22:21:00.205740

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2e8e3b7068c2'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Groups',
    sa.Column('gid', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=20), nullable=False),
    sa.Column('description', sa.Text(), nullable=False),
    sa.Column('priv', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('gid')
    )
    with op.batch_alter_table('Groups', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_Groups_name'), ['name'], unique=False)

    op.create_table('Nodes',
    sa.Column('nid', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=20), nullable=False),
    sa.Column('description', sa.Text(), nullable=False),
    sa.Column('avatar', sa.String(length=200), nullable=True),
    sa.Column('url', sa.String(length=20), nullable=False),
    sa.Column('post_count', sa.Integer(), nullable=True),
    sa.Column('parent', sa.Integer(), nullable=True),
    sa.Column('access_level', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('nid'),
    sa.UniqueConstraint('name')
    )
    with op.batch_alter_table('Nodes', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_Nodes_url'), ['url'], unique=True)

    op.create_table('Users',
    sa.Column('uid', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=20), nullable=False),
    sa.Column('password', sa.String(length=200), nullable=False),
    sa.Column('email', sa.String(length=100), nullable=False),
    sa.Column('avatar', sa.String(length=200), nullable=True),
    sa.Column('banned', sa.Integer(), nullable=True),
    sa.Column('bio', sa.Text(), nullable=True),
    sa.Column('level', sa.Integer(), nullable=False),
    sa.Column('priv', sa.Integer(), nullable=False),
    sa.Column('point', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('uid'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    with op.batch_alter_table('Users', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_Users_created_at'), ['created_at'], unique=False)

    op.create_table('Posts',
    sa.Column('pid', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=50), nullable=False),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('author', sa.Integer(), nullable=False),
    sa.Column('node', sa.Integer(), nullable=False),
    sa.Column('access_level', sa.Integer(), nullable=True),
    sa.Column('edited', sa.Boolean(), nullable=True),
    sa.Column('topped', sa.Boolean(), nullable=True),
    sa.Column('readonly', sa.Boolean(), nullable=True),
    sa.Column('sort', sa.Integer(), nullable=True),
    sa.Column('views', sa.Integer(), nullable=True),
    sa.Column('commented_at', sa.DateTime(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['author'], ['Users.uid'], ),
    sa.ForeignKeyConstraint(['node'], ['Nodes.nid'], ),
    sa.PrimaryKeyConstraint('pid')
    )
    with op.batch_alter_table('Posts', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_Posts_created_at'), ['created_at'], unique=False)
        batch_op.create_index(batch_op.f('ix_Posts_title'), ['title'], unique=False)

    op.create_table('UserGroups',
    sa.Column('uid', sa.Integer(), nullable=False),
    sa.Column('gid', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['gid'], ['Groups.gid'], ),
    sa.ForeignKeyConstraint(['uid'], ['Users.uid'], ),
    sa.PrimaryKeyConstraint('uid', 'gid')
    )
    op.create_table('Comments',
    sa.Column('cid', sa.Integer(), nullable=False),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('author', sa.Integer(), nullable=False),
    sa.Column('post', sa.Integer(), nullable=False),
    sa.Column('edited', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['author'], ['Users.uid'], ),
    sa.ForeignKeyConstraint(['post'], ['Posts.pid'], ),
    sa.PrimaryKeyConstraint('cid')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('Comments')
    op.drop_table('UserGroups')
    with op.batch_alter_table('Posts', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_Posts_title'))
        batch_op.drop_index(batch_op.f('ix_Posts_created_at'))

    op.drop_table('Posts')
    with op.batch_alter_table('Users', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_Users_created_at'))

    op.drop_table('Users')
    with op.batch_alter_table('Nodes', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_Nodes_url'))

    op.drop_table('Nodes')
    with op.batch_alter_table('Groups', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_Groups_name'))

    op.drop_table('Groups')
    # ### end Alembic commands ###
