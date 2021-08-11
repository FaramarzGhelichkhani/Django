from django.contrib import admin
from django_admin_listfilter_dropdown.filters import DropdownFilter, ChoiceDropdownFilter, RelatedDropdownFilter
from movie.models import *
from django.db.models import F
import decimal,datetime


## filter films base on release year
class Release_Year_Filter(admin.SimpleListFilter):
    title = 'Release Year'                  # a label for our filter
    parameter_name = 'Release_Year'         # will be used in the URL query.

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        result = []
        Queryset = Film.objects.values_list('release_year',flat=True).distinct()
        for q in Queryset:
            result.append((str(q),q))
        return sorted(result, key=lambda year: year[1])

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(release_year=self.value())
        return queryset



## filter films base on actor's name.
class Actor_Filter(admin.SimpleListFilter):
    title='actor'
    parameter_name = 'Actor'
    def lookups(self, request, model_admin):
        result=[]
        Querry = Actor.objects.all()
        for q in Querry:
            result.append((q.actor_id,q.first_name+' '+q.last_name))
        return result

    def queryset(self, request, queryset):
        if self.value():
             return queryset.filter(film_actor__actor_id__actor_id=self.value())

##action:update last_update to datetim.now()
def Update_time(modeladmin, request, queryset):
    return queryset.update(last_update=datetime.datetime.now())

@admin.register(Film)
class FilmAdmin(admin.ModelAdmin):
    list_display = ('__str__','release_year','rating')
    list_filter = (Release_Year_Filter,('rating',DropdownFilter),Actor_Filter)
    actions = ['Rise_rentel_rate','Discount_rentel_rate']

    def Rise_rentel_rate(self , request, queryset):
        queryset.update(rental_rate=F('rental_rate') * decimal.Decimal('1.25'))
    # Rise_rentel_rate.short_description = 'increase_25%_to_rental_rate'

    def Discount_rentel_rate(self , request, queryset):
        queryset.update(rental_rate = F('rental_rate') * decimal.Decimal('0.75'))
    # Discount_rentel_rate.short_description = 'decrease 25% to rental_rate'



admin.site.register(Actor)
admin.site.register(Category)
admin.site.register(Film_Actor)
admin.site.register(Film_Category)
admin.site.register(Inventory)
admin.site.register(Rental)
admin.site.register(Language)
admin.site.add_action(Update_time, 'Update_time')
