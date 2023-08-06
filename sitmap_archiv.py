# source myvenv/bin/activate
# python manage.py shell
# import sitmap_archiv
from django.conf import settings
from django.db import models
from filme.models import Film, Event
import datetime
import os



events = Event.objects.filter(termin__lte = datetime.datetime.now()).order_by('-termin')

f = open("media/sitemap-chronik.xml", "w")

f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
f.write('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
for event in events:
    f.write("    <url>\n")
    f.write("        <loc>https://www.kino35.de/film/event/"+str(event.pk)+"/detail</loc>\n")
    f.write("        <lastmod>"+event.termin.strftime('%Y-%m-%d')+"</lastmod>\n")
    f.write("        <changefreq>never</changefreq>\n")
    f.write("        <priority>0.1</priority>\n")
    f.write("    </url>\n")
f.write('</urlset>\n')
f.close()
f = open("media/sitemap-chronik.xml", "r")

print(f.read()) 

      







