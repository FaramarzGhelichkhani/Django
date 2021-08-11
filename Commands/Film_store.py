from movie.models import *
from django.core.management.base import BaseCommand
from django.db.models import F,Q,Count

class Command(BaseCommand):
    help = 'Create Query'

    def add_arguments(self, parser):
        parser.add_argument('number', type=int, help="Question number" )


    def handle(self, *args, **kwargs):
        q = kwargs['number']

        if q == 1:
            Q   =   Film.objects.order_by('-length')[0:10]
            self.stdout.write(self.style.SUCCESS("The  10 most lenghth film :  "))
            for i in Q:
                result=i.title
                self.stdout.write(self.style.SUCCESS("{} ".format(result)))
        elif q == 2:
            f       =       Film.objects.get(title='Fever Empire')
            fa      =       Film_Actor.objects.filter(film_id=f.film_id)
            ac      =       Actor.objects.filter(actor_id__in=fa.values_list('actor_id', flat=True))\
                            .order_by('first_name','last_name')
            casts   =       ac.values_list('first_name','last_name')
            self.stdout.write(self.style.SUCCESS("The actor's name of Fever Empire movie:  "))
            for i in casts:
                self.stdout.write(self.style.SUCCESS("{} {} ".format(i[0],i[1])))
        elif q == 3:
            Q   =   Rental.objects.values(Title=F('inventory_id__film_id__title'))\
                    .annotate(count_of_rental=Count('rental_id')).order_by('-count_of_rental')[0]
            self.stdout.write(self.style.SUCCESS("TThe most rental movie:  "))
            for key , value in Q.items():
                self.stdout.write(self.style.SUCCESS("{} : {} ".format(key, value)))
        # elif q==4:
        #     film_actor.objects.annotate(f_id=F('film_id__film_id')).values(ac1=F('actor_id'),\
        #     ac2=F('actor_id')).annotate(count=Count('f_id')).filter(count__gt=2)
        elif q==5:
            Q   =   Rental.objects.values(category_name=F('inventory_id__film_id__film_category__category_id__name'))\
            .annotate(rental_count=Count('rental_id')).order_by('-rental_count')[0]
            self.stdout.write(self.style.SUCCESS("The most favorite category base on count of rental:  "))
            for key , value in Q.items():
                self.stdout.write(self.style.SUCCESS("{} : {} ".format(key, value)))
        else:
            self.stdout.write(self.style.ERROR('error: should use [1-5] for qustion number.'))
