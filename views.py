from pyramid.response import Response
from pyramid.view import view_config

from pyramid.httpexceptions import HTTPFound
from .forms import EntryCreateForm

from sqlalchemy.exc import DBAPIError

from pyramid.httpexceptions import HTTPNotFound

from .models import (
	DBSession,
	MyModel,
	Entry,
	)

def view(request):
	this_id = request.matchdict.get('id', -1)
	entry = Entry.by_id(this_id)
	if not entry:
		return HTTPNotFound()
	return {'entry': entry}
    
def create(request):
	entry = Entry()
	form = EntryCreateForm(request.POST)
	if request.method == 'POST' and form.validate():
		form.populate_obj(entry)
		DBSession.add(entry)
		return HTTPFound(location=request.route_url('home'))
	return {'form': form, 'action': request.matchdict.get('action')}
    
#@view_config(route_name='action', match_param='action=create',
#             renderer='templates/edit.jinja2')
# @view_config(route_name='home', renderer='templates/mytemplate.pt')
# def my_view(request):
#     try:
#         one = DBSession.query(MyModel).filter(MyModel.name == 'one').first()
#     except DBAPIError:
#         return Response(conn_err_msg, content_type='text/plain', status_int=500)
#     return {'one': one, 'project': 'learning_journal'}

#@view_config(route_name='home', renderer='string')
#def index_page(request):
#    return 'list page'

@view_config(route_name='home', renderer='string')
def index_page(request):
	entry_id = request.matchdict['id']
	entries = Entry.all()
	entry = Entry.by.id(entry_id)
	if not Entry:
		return HTTPNotFound()
	return {'entries': entries}

@view_config(route_name='detail', renderer='string')
def view(request):
	return 'detail page'

@view_config(route_name='action', match_param='action=create', renderer='string')
def create(request):
	return 'create page'

@view_config(route_name='action', match_param='action=edit', renderer='string')
def update(request):
	return 'edit page'
    
conn_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to run the "initialize_learning_journal_db" script
    to initialize your database tables.  Check your virtual
    environment's "bin" directory for this script and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""

