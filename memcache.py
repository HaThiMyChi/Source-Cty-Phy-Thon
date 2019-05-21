__author__ = 'DUY'

from google.appengine.api import memcache
import logging

def get_greetings(self, guestbook_name):
	greetings = memcache.get('{}:greetings'.format(guestbook_name))
	if greetings is None:
		greetings = self.render_greetings(guestbook_name)
		try:
			added = memcache.add(
				'{}:greetings'.format(guestbook_name), greetings, 10)
			if not added:
				logging.error('Memcache set failed.')
		except ValueError:
			logging.error('Memcache set failed - data larger than 1MB')
	return greetings