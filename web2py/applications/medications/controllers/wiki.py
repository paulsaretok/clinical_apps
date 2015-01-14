def index():
     """ this controller returns a dictionary rendered by the view
         it lists all wiki pages
     >>> index().has_key('pages')
     True
     """
     pages = db().select(db.page.id,db.page.title,orderby=db.page.title)
     return dict(pages=pages)

@auth.requires_login()
def create():
     """creates a new empty wiki page"""
     form = SQLFORM(db.page).process(next=URL('index'))
     return dict(form=form)

def show():
     """shows a wiki page"""
     this_page = db.page(request.args(0,cast=int)) or redirect(URL('index'))
     db.post.page_id.default = this_page.id
     form = SQLFORM(db.post).process() if auth.user else None
     pagecomments = db(db.post.page_id==this_page.id).select()
     return dict(page=this_page, comments=pagecomments, form=form)

@auth.requires_login()
def edit():
     """edit an existing wiki page"""
     this_page = db.page(request.args(0,cast=int)) or redirect(URL('index'))
     form = SQLFORM(db.page, this_page).process(
         next = URL('show',args=request.args))
     return dict(form=form)

@auth.requires_login()
def documents():
     """browser, edit all documents attached to a certain page"""
     page = db.page(request.args(0,cast=int)) or redirect(URL('index'))
     db.document.page_id.default = page.id
     db.document.page_id.writable = False
     grid = SQLFORM.grid(db.document.page_id==page.id,args=[page.id])
     return dict(page=page, grid=grid)

def user():
     return dict(form=auth())

def download():
     """allows downloading of documents"""
     return response.download(request, db)

def search():
     """an ajax wiki search page"""
     return dict(form=FORM(INPUT(_id='keyword',_name='keyword',
              _onkeyup="ajax('callback', ['keyword'], 'target');")),
              target_div=DIV(_id='target'))

def callback():
     """an ajax callback that returns a <ul> of links to wiki pages"""
     query = db.page.title.contains(request.vars.keyword)
     pages = db(query).select(orderby=db.page.title)
     links = [A(p.title, _href=URL('show',args=p.id)) for p in pages]
     return UL(*links)
