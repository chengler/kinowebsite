from django.contrib import admin

# Register your models here.
from django_summernote.admin import SummernoteModelAdmin
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


class InhaltsseiteAdmin(SummernoteModelAdmin):
     summernote_fields = ('text',)

# # Apply summernote to all TextField in model.
# class SomeModelAdmin(SummernoteModelAdmin):  # instead of ModelAdmin
#     summernote_fields = '__all__'
# # Apply summernote only to specific TextField in model
# https://github.com/summernote/django-summernote


admin.site.register(Film, FilmAdmin)
admin.site.register(Inhaltsseite, InhaltsseiteAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(NewsletterAbonnent, NewsletterAdmin)
admin.site.register(NewsletterSent)



