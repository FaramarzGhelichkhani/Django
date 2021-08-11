from rest_framework.decorators import action
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import *
from .models import Film, Actor, Category, Film_Category, Film_Actor
import datetime


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class FilmViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Film to be viewd or edited.
    """
    queryset = Film.objects.all()
    serializer_class = FilmSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=['GET', 'POST', 'DELETE'])
    def actor_list(self, request, pk=None):
        """
        get actors list for a film .
        insert or delet actors for a film.
        """
        film_id = pk
        if request.method == 'GET':
            actors = Actor.objects.filter(film_actor__film_id=film_id)
            serializer = ActorSerializer(actors, many=True)
            return Response(serializer.data)
        elif request.method == 'POST':
            film_act = Film_Actor.objects.filter(film_id=film_id)
            serializer = FilmActorSerializer(film_cat, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response('sucessfuly added', serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        elif request.method == 'DELETE':
            film_act.delete()
            return Response('Sucessfuly Deleted', status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['GET', 'POST', 'DELETE'])
    def category(self, request, pk=None):
        """
        get gategory list for a film.
        insert or delete a category.
        """
        film_id = pk
        if request.method == 'GET':
            cats = Category.objects.filter(film_category__film_id=film_id)
            serializer = CategorySerializer(cats, many=True)
            return Response(serializer.data)
        elif request.method == 'POST':
            film_cat = Film_Category.objects.filter(film_id=film_id)
            serializer = FilmCategorySerializer(film_cat, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response('sucessfuly added', serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        elif request.method == 'DELETE':
            film_cat.delete()
            return Response('Sucessfuly Deleted', status=status.HTTP_204_NO_CONTENT)


class ActorViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Actor to be viewd or edited
    """
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=['GET'])
    def film_list(self, request, pk=None):
        """
        get films list for an actor .
        """
        actor_id = pk
        films = Film.objects.filter(film_actor__actor_id=actor_id)
        serializer = FilmSerializer(films, many=True)
        return Response(serializer.data)


class CategoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Category to be viewed or edited
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]


@api_view(['POST'])
def insertmovie(request, film_id, actor_id, category_id, format=None):
    """
    insert a film with actor and category in film_actor and film_category tabels.
    """
    if request.method == 'POST':
        film_actor = Film_Actor.objects.get(film_id=film_id, actor_id=actor_id)
        film_category = Film_Category.get(film_id=film_id, category_id=category_id)
        if film_actor and film_category:
            return Response({"message": "there is such a data already exist."}, status=HTTP_400_BAD_REQUEST)

        elif film_actor == False and film_category == False:
            film_act = Film_Actor.objects.create(film_id=film_id, actor_id=actor_id,
                                                 last_update=datetime.datetime.now())
            film_cat = Film_Category.objects.create(film_id=film_id, category_id=category_id,
                                                    last_update=datetime.datetime.now())
            serializer1 = FilmActorSerializer(film_act)
            serializer2 = FilmCategorySerializer(film_cat)
            if serializer1.is_valid() and serializer2.is_valid():
                serializer1.save()
                serializer2.save()
                return Response('sucessfuly added', status=status.HTTP_201_CREATED)
            return Response([serializer1.errors, serializer2.errors], status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=HTTP_400_BAD_REQUEST)
    else:
        return Response(status=HTTP_400_BAD_REQUEST)
