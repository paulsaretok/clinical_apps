@auth.requires_login()
def index():
    images = db().select(db.image.ALL, orderby=db.image.title)
    return dict(images=images)

@auth.requires_login()
def show():
    image = db.image(request.args(0,cast=int)) or redirect(URL('index'))
    db.post.image_id.default = image.id
    form = SQLFORM(db.post)
    if form.process().accepted:
        response.flash = 'your comment is posted'
    comments = db(db.post.image_id==image.id).select()
    return dict(image=image, comments=comments, form=form)

@auth.requires_login()
def download():
    return response.download(request, db)

@auth.requires_membership('manager')
def manage():
    grid = SQLFORM.smartgrid(db.image,linked_tables=['post'])
    return dict(grid=grid)

def user():
    return dict(form=auth())


