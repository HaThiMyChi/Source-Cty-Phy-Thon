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

import logging
from google.appengine.api import search
from google.appengine.api import memcache
import json

def create_player(player):
	# logging.debug(player)
	player = search.Document(
		doc_id = str(player.key.id()),
	    fields=[
		    search.TextField(name='name', value= player.name),
	        search.NumberField(name='age', value=player.age),
	        search.TextField(name='national', value=player.national),
	        search.TextField(name='position', value=player.position),
	        search.NumberField(name='salary', value=player.salary)
	    ])
	return player

def add_player_to_index(player):
	index = search.Index('players')
	# memcache.add(key="ABC", value="name")
	index.put(player)

def delete_index( doc_id):
	index = search.Index('players')
	index.delete(doc_id)

def get_list_player():
	index = search.Index('players')
	query_string = 'name: Kim Thi'
	results = index.search(query_string)
	# logging.debug(results)
	return results

#index chinh la search.Index('players')
def query_offset(current_page,page_size):
	index = search.Index('players')
	# query_string = 'name: Kim Thi'
	query_string = ''
	# query_string = index.search()
	# offset = 0
	# page_size = 10
	# Build the query using the current offset.
	offset = (current_page - 1)*page_size
	# while True:
	# options = search.QueryOptions(offset=offset, limit=page_size)
	options = search.QueryOptions(offset=offset, limit=page_size)
	query = search.Query(query_string=query_string, options=options)
	results = index.search(query)

	# calculate pages
	# number_page = results.number_found / page_size

	count = results.number_found
	number_page =  int(count/ page_size) + (count % page_size > 0)

	users_array = []
	# Process the matched documents
	for row in results:
		# logging.debug(row)
		id = row.doc_id,
		name = row.field('name').value
		age = row.field('age').value
		national = row.field('national').value
		position = row.field('position').value
		salary = row.field('salary').value

		# logging.debug(id, name, age, national, position, salary)

		users_array.append({
			'id': id,
			'name':name,
			'age': age,
			'national': national,
			'position': position,
			'salary': salary,
		})
	data ={
		'number_page':number_page,
	    'players':users_array,
		'current_page':current_page
	}
	users_list = json.JSONEncoder().encode(data)
	logging.debug(users_list)
	return users_list

def search_name(current_page,page_size, key_word, type):
	index = search.Index('players')
	# query_string = 'name: Kim Thi'
	# name = "name:"
	# query_string = " " + name + key_word + " "
	if type == "name":
		query_string = "name:" + key_word
	elif type == "age":
		query_string = "age:" + key_word
	elif type == "national":
		query_string = "national:" + key_word
	elif type == "position":
		query_string = "position:" + key_word
	else:
		query_string = "salary:" + key_word
	# query_string = "name:" + key_word

	# query_string = "name:" + key_word  #search theo name

	# logging.debug(query_string)
	# Build the query using the current offset.
	offset = (current_page - 1)*(page_size)
	# while True:
	# options = search.QueryOptions(offset=offset, limit=page_size)
	options = search.QueryOptions(offset=offset, limit=page_size)
	query = search.Query(query_string=query_string, options=options)
	results = index.search(query)

	# calculate pages
	# number_page = results.number_found / page_size

	count = results.number_found
	number_page =  int(count/ page_size) + (count % page_size > 0)

	users_array = []
	# Process the matched documents
	for row in results:
		# logging.debug(row)
		id = row.doc_id,
		name = row.field('name').value
		age = row.field('age').value
		national = row.field('national').value
		position = row.field('position').value
		salary = row.field('salary').value

		# logging.debug(id, name, age, national, position, salary)

		users_array.append({
			'id': id,
			'name':name,
			'age': age,
			'national': national,
			'position': position,
			'salary': salary,
		})
	data ={
		'number_page':number_page,
	    'players':users_array,
		'current_page':current_page
	}
	users_list = json.JSONEncoder().encode(data)
	logging.debug(users_list)
	return users_list











