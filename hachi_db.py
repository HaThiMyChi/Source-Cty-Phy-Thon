import os
import jinja2
cwd = os.path.dirname(__file__)
path = os.path.join(cwd, 'templates')
jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(path))


import webapp2
from google.appengine.ext import ndb

import snippets


class HachiBook(ndb.Model):
	username = ndb.StringProperty()
	userid = ndb.VMSG_RECEIVER_SEARCH_LIST()
	email = ndb.StringProperty()

def create_entity_book():
	book = HachiBook(
		username='Sandy', userid=123, email='sandy@example.com')
	return book





