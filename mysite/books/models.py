from django.db import models

# Create your models here.
class book_model():
	def __init__(self,dict):
		self.isbn = dict['isbn']
		self.title = dict['title']
		self.author = dict['author']
		self.release_year = dict['release_year']
		self.publisher = dict['publisher']
		self.image = dict['Image-URL-L']

