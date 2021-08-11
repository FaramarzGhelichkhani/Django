from django.contrib.auth.models import User, Group
from rest_framework import serializers
from  .models import Film,Actor,Category,Film_Category,Film_Actor

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']



class FilmSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Film
        fields=['film_id','title','description','release_year','language_id','rental_duration','rental_rate','length',\
               'replacement_cost','rating','last_update','special_features','fulltext']


class ActorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Actor
        fields=['actor_id','first_name','last_name','last_update']



class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields=['category_id','name','last_update']


class FilmCategorySerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model=Film_Category
		fields=['film_id','category_id','last_update']

class FilmActorSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model=Film_Actor
		fields=['film_id','actor_id','last_update']
