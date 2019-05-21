# Copyright 2016 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import jinja2

cwd = os.path.dirname(__file__)
path = os.path.join(cwd, 'templates')
jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(path))

import search
import webapp2
from player import Player

import logging

import datetime
import urllib
# import snippets


class MainPage(webapp2.RequestHandler):

	def get(self):
		template = jinja_environment.get_template('index.html')
		values ={'abc':'hello'}
		#snippets.fetch_good_articles_using_gql_with_inlined_bind()
		self.response.out.write(template.render(values))

	def post(self):
		pass

class AddPlayer(webapp2.RequestHandler):
	def get(self):
		template = jinja_environment.get_template('add.html')
		# players = self.get_player()
		# for player in players:

		#snippets.fetch_good_articles_using_gql_with_inlined_bind()
		self.response.out.write(template.render())

	def post(self):
		name = self.request.get('name')
		age = self.request.get('age')
		# str(age)
		national = self.request.get('national')
		position = self.request.get('position')
		salary = self.request.get('salary')
		# str(salary)
		params = {
			'name': name,
			'age': age,
		    'national': national,
		    'position': position,
		    'salary': salary
		}
		logging.debug(params)
		player = Player.add_player(params)
		data = search.create_player(player)
		search.add_player_to_index(data)
		# search.add_player_and_get_doc_id(data)

		self.redirect('/')

class ListPlayer(webapp2.RequestHandler):
	def get(self):
		list_players = Player.getListPlayer()
		values = {
            'players':list_players
        }
		template = jinja_environment.get_template('index.html')
		self.response.out.write(values)

	def post(self):
		pass

class ListPlayerData(webapp2.RequestHandler):
	def get(self):
		current_page = self.request.get('page')
		page_size = self.request.get('page_size')
		current_page = int(current_page)
		page_size = int(page_size)

		# list_players = Player.getListPlayerJSON(current_page,page_size)

        # values = {
        #     'players':list_players
        # }
		# template = jinja_environment.get_template('index.html')
		#self.response.out.write(list_players)

		# resulttest = search.get_list_player()
		query_list = search.query_offset(current_page,page_size)
		self.response.out.write(query_list)

	def post(self):
		pass

class RemovePlayer(webapp2.RequestHandler):
	def get(self):
		id = self.request.get('id')
		deleted = Player.remove_player(id)
		if deleted is True:
			search.delete_index(id)
		self.redirect('/')


class EditPlayer(webapp2.RequestHandler):
	# def get(self):
	# 	id = self.request.get('id')
	# 	# logging.debug(id)
	# 	player = Player.get_by_id(int(id))
	# 	values = {'player': player.to_dict()}
	# 	template = jinja_environment.get_template('edit.html')
	# 	self.response.out.write(template.render(values))
	def post(self):
		id = self.request.get('id')
		name = self.request.get('name')
		age = self.request.get('age')
		national = self.request.get('national')
		position = self.request.get('position')
		salary = self.request.get('salary')
		params ={
			'id': id,
			'name': name,
			'age': age,
		    'national': national,
		    'position': position,
		    'salary': salary
		}
		logging.debug(id)
		logging.debug(params)
		player = Player.edit_player(params)
		if player is not None:
			data = search.create_player(player)
			search.add_player_to_index(data)
		self.redirect('/')

# class SearchPlayer(webapp2.RequestHandler):
# 	def post(self):
# 		key_word = self.request.get('key_word')
# 		current_page = self.request.get('page')
# 		page_size =  self.request.get('page_size')
# 		type =  self.request.get('type')
# 		current_page = int(current_page)
# 		page_size = int(page_size)
#
# 		query_list = search.search_name(current_page,page_size, key_word, type)
# 		# logging.debug(query_list)
# 		self.response.out.write(query_list)

class SearchPlayerFilter(webapp2.RequestHandler):
	def post(self):
		key_word = self.request.get('key_word')
		current_page = self.request.get('page')
		page_size =  self.request.get('page_size')
		type =  self.request.get('type')
		current_page = int(current_page)
		page_size = int(page_size)
		# key_word = self.request.get('key_word')
		query_search = Player.search_player(current_page, page_size, key_word, type)
		# query_search = Player.search_player(key_word)
		self.response.out.write(query_search)

class Script(webapp2.RequestHandler):

	def get(self):
		template = jinja_environment.get_template('script.html')
		values ={'abc':'hello'}
		self.response.out.write(template.render(values))


	def post(self):
		pass

class SubmitForm(webapp2.RequestHandler):
	def post(self):
	 	pass

app = webapp2.WSGIApplication([
	('/script', Script),
    ('/', MainPage),
    ('/sign', SubmitForm),
    ('/create', AddPlayer),
    ('/remove', RemovePlayer),
    # ('/add', AddPlayer),
    ('/add', AddPlayer),
	('/list', ListPlayer),
	('/getlist', ListPlayerData),
    ('/edit', EditPlayer),
	# ('/search', SearchPlayer),
    ('/search', SearchPlayerFilter),
], debug=True)
