# source myvenv/bin/activate
# python manage.py shell
# import change_category_in_DB
from django.conf import settings
from django.db import models
from filme.models import Film, Event
import datetime

e = Event.objects.get(pk=220)
e.kategorie = 7
e.save()
e = Event.objects.get(pk=512)
e.kategorie = 4
e.save()
e = Event.objects.get(pk=504)
e.kategorie = 4
e.save()
e = Event.objects.get(pk=196)
e.kategorie = 4
e.save()

events = Event.objects.filter(termin__lte = datetime.datetime.now()).order_by('-termin')
for event in events:
    #if (event.termin.weekday() == 4) and (event.termin.time() != datetime.time(20, 30) ) and (event.termin.time() != datetime.time(20, 0)):
    if (event.termin.weekday() == 4):
        event.kategorie = 1
        event.save()
        print(event.pk, ' ',event.kategorie, ' ' , event.film)
    elif (event.termin.weekday() == 6):
        event.kategorie = 2
        event.save()
        print(event.pk, ' ',event.kategorie, ' ' , event.film)
    elif (event.kategorie == None):
        event.kategorie = 3
        event.save()
  




