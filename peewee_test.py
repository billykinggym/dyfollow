import datetime
import unittest

from entity.UserEntity import User, WorkItems
from entity.db import db

db.connect()
db.create_tables([User, WorkItems])

def creareUser():
	user = User(mainurl='user1', count=0)
	user_id = user.save()
	print(user_id)


class TestMyFunction(unittest.TestCase):
	def test_queryUser(self):
		user = User.get_or_none(User.mainurl == 'user11')
		print(user.id)

	def test_updateUser(self):
		user = User.get_or_none(User.mainurl == 'user1')
		user.count=6
		user.save()
		user = User.get_or_none(User.mainurl == 'user1')
		print(user.count)

	def test_createWorkItem(self):
		w = WorkItems(url="test",userid=0,like=0)
		w.save()
		w.like=3
		w.save()


	def test_updateWorkItem(self):
		w = WorkItems.get_or_none(WorkItems.url =="test")
		w.last_access_time = datetime.datetime.now()
		w.save()