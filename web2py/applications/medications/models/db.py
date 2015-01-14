db = DAL("sqlite://storage.sqlite")

db.define_table('image',
   Field('title', unique=True),
   Field('file', 'upload'),
   format = '%(title)s')

db.define_table('image_post',
   Field('image_id', 'reference image'),
   Field('author'),
   Field('email'),
   Field('body', 'text'))

db.image.title.requires = IS_NOT_IN_DB(db, db.image.title)
db.image_post.image_id.requires = IS_IN_DB(db, db.image.id, '%(title)s')
db.image_post.author.requires = IS_NOT_EMPTY()
db.image_post.email.requires = IS_EMAIL()
db.image_post.body.requires = IS_NOT_EMPTY()

db.image_post.image_id.writable = db.image_post.image_id.readable = False

from gluon.tools import *
auth = Auth(db)
auth.define_tables(username=True)
crud = Crud(db)

db.define_table('page',
    Field('title'),
    Field('body', 'text'),
    Field('created_on', 'datetime', default=request.now),
    Field('created_by', 'reference auth_user', default=auth.user_id),
    format='%(title)s')

db.define_table('post',
    Field('page_id', 'reference page'),
    Field('body', 'text'),
    Field('created_on', 'datetime', default=request.now),
    Field('created_by', 'reference auth_user', default=auth.user_id))

db.define_table('document',
    Field('page_id', 'reference page'),
    Field('name'),
    Field('file', 'upload'),
    Field('created_on', 'datetime', default=request.now),
    Field('created_by', 'reference auth_user', default=auth.user_id),
    format='%(name)s')

db.page.title.requires = IS_NOT_IN_DB(db, 'page.title')
db.page.body.requires = IS_NOT_EMPTY()
db.page.created_by.readable = db.page.created_by.writable = False
db.page.created_on.readable = db.page.created_on.writable = False

db.post.body.requires = IS_NOT_EMPTY()
db.post.page_id.readable = db.post.page_id.writable = False
db.post.created_by.readable = db.post.created_by.writable = False
db.post.created_on.readable = db.post.created_on.writable = False

db.document.name.requires = IS_NOT_IN_DB(db, 'document.name')
db.document.page_id.readable = db.document.page_id.writable = False
db.document.created_by.readable = db.document.created_by.writable = False
db.document.created_on.readable = db.document.created_on.writable = False

db.define_table('thing',Field('name',requires=IS_NOT_EMPTY()))