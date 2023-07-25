from django.contrib import admin

# Register your models here.
from .models import Film,  Inhaltsseite, Event, NewsletterAbonnent, NewsletterSent



class FilmAdmin(admin.ModelAdmin):
    search_fields = ['name', 'status']
    fieldsets = [
        (None,               {'fields': ['name']}),
        ('Löschschutz', {'fields': ['film_no_delete']}),
        ('Beschreibung', {'fields': ['description']}),


    ]
    list_display = ('name', 'status', 'film_no_delete')


class EventAdmin(admin.ModelAdmin):
    search_fields = ['termin', 'kategorie']
    list_display = ('termin', 'film', 'event_online', 'kategorie')
    fieldsets = [
        (None,               {'fields': ['termin']}),
        ('Film', {'fields': ['location_address']}),
    ]

class NewsletterAdmin(admin.ModelAdmin):
    search_fields = ['email',]
    list_display = ('email', 'beantragt', 'opt_in')






admin.site.register(Film, FilmAdmin)
admin.site.register(Inhaltsseite)
admin.site.register(Event, EventAdmin)
admin.site.register(NewsletterAbonnent, NewsletterAdmin)
admin.site.register(NewsletterSent)



