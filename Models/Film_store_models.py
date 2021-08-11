from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.postgres.search import SearchVectorField


class Film(models.Model):
	film_id			=	models.IntegerField( primary_key=True)
	title			=	models.CharField(max_length=255)			#character varying
	description		=	models.TextField()				#text		nullable
	release_year	=	models.IntegerField(null=True)		#year		nullable
	language_id		=	models.SmallIntegerField()			#smallint
	rental_duration	=	models.SmallIntegerField(default=3)	#smallint
	rental_rate		=	models.DecimalField(max_digits='4',decimal_places='2',default=4.99)		#numeric(2,4)
	length			=	models.SmallIntegerField(null=True)		#smallint	nullable
	replacement_cost=   models.DecimalField(max_digits='5',decimal_places='2',default=19.99)	#numeric(2,5)
	rating			=	models.CharField(max_length=50)
	last_update		=	models.DateTimeField()			#default=datetime.now
	special_features= 	ArrayField(models.CharField(max_length = 1000), default = list) #text[]
	fulltext		=	SearchVectorField() 	#type : tsvector


	def __str__(self):
		return '{}'.format(self.title)


class Film_Actor(models.Model):
	film_id		=	models.ForeignKey('Film',on_delete=models.RESTRICT)
	actor_id	=	models.ForeignKey('Actor',on_delete=models.RESTRICT)
	last_update	=	models.DateTimeField()

	class Meta:
		unique_together = (("film_id", "actor_id"),)



	def __str__(self):
		return '{} , {}'.format(self.film_id,self.actor_id)

class Actor(models.Model):
	actor_id		=	models.IntegerField( primary_key=True)
	first_name		=	models.CharField(max_length=45)
	last_name		=	models.CharField(max_length=45)
	last_update		=	models.DateTimeField()


	def full_name(self):
		return self.first_name + ' ' + self.last_name


	def __str__(self):
		return '{}'.format(self.actor_id)


class Category(models.Model):
	category_id		=	models.IntegerField( primary_key=True,auto_created=True)
	name			=	models.CharField(max_length=25)
	last_update		=	models.DateTimeField(null=True)

	def __str__(self):
		return '{}'.format(self.category_id)
class Film_Category(models.Model):
	film_id		=	models.ForeignKey('Film',on_delete=models.RESTRICT)
	category_id	=	models.ForeignKey('Category',on_delete=models.RESTRICT)
	last_update	= 	models.DateTimeField()

	class Meta:
		unique_together = (("film_id", "category_id"),)

	def __str__(self):
		return 'film id: {} , category id:{}'.format(self.film_id,self.category_id)

class Inventory(models.Model):
	inventory_id 	= models.IntegerField( primary_key=True)
	film_id			= models.ForeignKey('Film',on_delete=models.RESTRICT)
	store_id 		= models.SmallIntegerField()
	last_update 	= models.DateTimeField()

	def __str__(self):
		return '{}'.format(self.inventory_id)

class Rental(models.Model):
	rental_id		= models.IntegerField( primary_key=True)
	rental_date		= models.DateTimeField()
	inventory_id	= models.ForeignKey('Inventory',on_delete=models.RESTRICT)
	customer_id		= models.SmallIntegerField()
	return_date		= models.DateTimeField(null=True)
	staff_id    	= models.SmallIntegerField()
	last_update  	= models.DateTimeField()

	def __str__(self):
		return '{}'.format(self.rental_id)

class Language(models.Model):
	language_id	=	models.ForeignKey('Film',on_delete=models.RESTRICT)
	name		=	models.CharField(max_length=20)
	last_update	=	models.DateTimeField()


	def __str__(self):
		return self.name
