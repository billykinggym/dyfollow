import datetime

from peewee import CharField, IntegerField, AutoField, Model, DateTimeField

from entity.db import db

class User(Model):
	id= AutoField(primary_key=True)
	mainurl = CharField(unique=True)
	count = IntegerField()
	last_access_time = DateTimeField(default=datetime.datetime.now)
	class Meta:
		database = db


class WorkItems(Model):
	url = CharField(unique=True)
	userid = IntegerField(index=True)
	title = CharField(null=True)
	like = CharField(null=True)
	downloadpath = CharField(null=True)
	last_access_time = DateTimeField(default=datetime.datetime.now)
	class Meta:
		database = db