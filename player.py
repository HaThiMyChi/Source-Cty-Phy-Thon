__author__ = 'DUY'
from google.appengine.ext import ndb
import json
import logging
from google.appengine.api import search

class Player(ndb.Model):
	name = ndb.StringProperty()
	age = ndb.IntegerProperty()
	national = ndb.StringProperty()
	position = ndb.StringProperty()
	salary = ndb.IntegerProperty()


	@classmethod
	def add_player(cls, params):
		player = cls()
		player.name = params['name']
		player.age = int(params['age'])
		player.national = params['national']
		player.position = params['position']
		player.salary = int(params['salary'])
		player.put()
		return player

	@classmethod
	def getListPlayer(cls):
		query = cls.query()
		q = query.fetch()
		users_array = []
		for row in q:
			users_array.append({
				'id': row.key.id(),
                'name': row.name,
                'age': row.age,
			    'national': row.national,
			    'position': row.position,
			     'salary': row.salary,
			})
		# users_list = json.JSONEncoder().encode(users_array)
		return users_array

	# @classmethod
	def getListPlayerJSON(cls,current_page,page_size):
		query = cls.query()
		count = query.count()
		number_page =   int(count/ page_size) + (count % page_size > 0)
		offset = (current_page - 1)*page_size
		q = query.fetch(page_size, offset = offset)
		users_array = []
		for row in q:
			users_array.append({
				'id': row.key.id(),
                'name': row.name,
                'age': row.age,
			    'national': row.national,
			    'position': row.position,
			     'salary': row.salary,
			})
		data ={
			'number_page':number_page,
		    'players':users_array,
			'current_page':current_page
		}
		users_list = json.JSONEncoder().encode(data)
		return users_list

	@classmethod
	def remove_player(cls, id):
		logging.debug('remove_player='+ id)
		player = cls.get_by_id(int(id))
		if player is not None:
			player.key.delete()
			return True
		else:
			logging.debug('remove_player= id None')
		return False

	@classmethod
	def edit_player(cls, id, params):
		player = cls.get_by_id(int(id))
		if player is not None:
			player.name = params['name']
			player.age = int(params['age'])
			player.national = params['national']
			player.position = params['position']
			player.salary = int(params['salary'])
			player.put()
		return player

	@classmethod
	def search_player(cls, current_page, page_size, key_word, type):
		# logging.basicConfig(level=logging.DEBUG)
		# logging.debug(type(key_word)) #logging type la unicode ma chua log dc xem lai
		query =  cls.query()
		filter = None
		if type == 'all':
			# if isinstance(key_word, int):
			# if isinstance(key_word, (int, long, float)) :
			if key_word.isdigit() :
				key_word = int(key_word)
				filter = query.filter(ndb.OR(cls.name == str(key_word), cls.age == key_word, cls.position == str(key_word), cls.national == str(key_word), cls.salary == key_word))
			else :
				filter = query.filter(ndb.OR(cls.name == key_word, cls.position == key_word, cls.national == key_word))
		else:
			if type == "name":
				query_string = cls.name
			elif type == "age":
				query_string = cls.age
				key_word = int(key_word)
			elif type == "national":
				query_string = cls.national
			elif type == "position":
				query_string = cls.position


			else :
				query_string = cls.salary
				key_word = int(key_word)
			filter = query.filter(query_string == key_word)
		count = filter.count()
		# logging.debug(count)
		number_page =  int(count/ page_size) + (count % page_size > 0)
		offset = (current_page - 1)*page_size
		q = filter.fetch(page_size, offset = offset)
		users_array = []
		for row in q:
			users_array.append({
				'id': row.key.id(),
                'name': row.name,
                'age': row.age,
			    'national': row.national,
			    'position': row.position,
			     'salary': row.salary,
			})
		data ={
			'number_page':number_page,
		    'players':users_array,
			'current_page':current_page
		}
		users_list = json.JSONEncoder().encode(data)
		return users_list

