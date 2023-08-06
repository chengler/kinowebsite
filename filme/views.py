from django.shortcuts import redirect, render, get_object_or_404
from django.utils import timezone
from .models import Film, Event, Comment, Inhaltsseite, NewsletterAbonnent, NewsletterSent  , ZeitStempel, Sondernewsletter
from .forms import *
# FilmForm, FilmNeuForm, FilmBewertungForm, EventForm, CommentForm, SpielplanForm, EventNeuForm, EventDiensteForm
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse  #, HttpResponseForbidden # klingt interessant
import datetime
import requests
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import User
import os
from mysite.newsletter_keys import *
# import filter
from django.conf import settings

from django.contrib.auth import get_user_model

from dateutil import parser
from django.db import IntegrityError
from html.parser import HTMLParser
from html.entities import name2codepoint
from bs4 import BeautifulSoup
# import bild über url
from io import BytesIO
from urllib.request import urlopen
from django.core.files import File
from django.contrib import messages
import threading
# from datetime import datetime
from django.forms import modelformset_factory
import logging
from logging import FileHandler
# import logging.handlers
logger = logging.getLogger(__name__) 
#     logger.info("Text:  request.user  %s", request.user)


def error404(request, exception):
    return render(request, 'filme/404.html', exception = exception)


def newsletter_form_snippet(request):
    ''' handels die newsletter form und leitet
    zur feedbackseite weiter mit flag=status'''
    form = NewsletterAboForm(request.POST)
    if form.is_valid():
        abo = form.save(commit=False)
        abo.save()
        flag = 'neu'
        user = NewsletterAbonnent.objects.get(email = abo.email) 
        user.salz = BaseUserManager().make_random_password() # erhält passwort
        user.save()
        user.sent_opt_in()
        print('flag', flag)
        return redirect( 'newsletter_abo_feedback', flag = flag)
    else: # check bounce!
        email = request.POST['email']
        flag="error"
        user = NewsletterAbonnent.objects.get(email = email)
        if user.opt_in:
            flag="OK"
        else:
            flag="wartend"
            user.sent_opt_in()
        print('flag', flag)
        return redirect( 'newsletter_abo_feedback', flag = flag)

def film_index(request):
    ''' Die Startseite zeigt den Event/die Events 
    des nächsten Spieltages'''
    # nextevents alle verantaltungen des nächsten Veranstaltungstages
    nextevents = get_programm_query()
    sidebar_events = get_sidebar_query(1)
    # 0 wenn 0 oder gerade dann newsletterabo in eigene zeile
    sidebar_count = len(sidebar_events) % 2
    if nextevents:
        datum = nextevents[0].termin.date() # hole Tag
        events = Event.objects.filter(event_online=True, termin__date = datum).order_by('termin')
    else: 
        events = nextevents # empty
        # print('kein Film mehr im aktuellen Programm')
        logger.info("film_index: Keine Filme mehr im aktuellen Programm")

        
    hinweis = Inhaltsseite.objects.filter(typen = 1)
    if hinweis:
        hinweis = hinweis[0]  
    else:
        print("Keine Hinweise enthalten")
    if request.method == "POST":
        return newsletter_form_snippet(request)
    else:
        form = NewsletterAboForm()
    return render(request, 'filme/film_index.html', {'events': events, 'hinweis': hinweis, 
      'form': form, 'sidebar_count': sidebar_count,'sidebar_events': sidebar_events})

def filmevent_programm_list(request):
    ''' Die Programmübersicht'''
    nextevents = get_programm_query()
    sidebar_events = get_sidebar_query(0)
    # 0 wenn 0 oder gerade dann newsletterabo in eigene zeile
    sidebar_count = len(sidebar_events) % 2
    if request.method == "POST":
        return newsletter_form_snippet(request)
    else:
        form = NewsletterAboForm()
    return render(request, 'filme/filmevent_programm_list.html',
     {'events': nextevents, 'sidebar_events': sidebar_events, 'sidebar_count': sidebar_count, 'form': form })

def newsletter_abo_feedback(request, flag):
    ''' Feedback nach Webanmeldung für den Newsletter'''
    print('newsletter_abo_feedback ', flag)
    return render(request, 'filme/newsletter_abo_feedback.html', { 'flag': flag })


    

def newsletters_opt_in(request, email, salz):
    ''' Feedback nach der Anmeldebestätigung
     via Email zum Newsletter'''
    status = "unbekannter Fehler; sorry"
    if NewsletterAbonnent.objects.filter(email=email).exists():
        abonnent = NewsletterAbonnent.objects.get(email=email)
        status = abonnent.empfange_opt_in(salz)
    else:
        status="Diese Email-Addresse wurde nicht gefunden. Vielleicht war der Anmeldelink zu alt. Bitte erneut auf der Startseite registrieren. Alternativ können Sie uns auch anmailen oder im Kino ansprechen."
    return render(request, 'filme/newsletter_opt_in.html', { 'email': email, 'status': status })

def newsletter_unsubscribe(request, email, salz):
    ''' Aus dem Newsletter löschen'''
    status = "unbekannter Fehler; sorry"
    if NewsletterAbonnent.objects.filter(email=email).exists():
        abonnent = NewsletterAbonnent.objects.get(email=email)
        status = abonnent.unsubscribe(salz)
    else:
        status="Sie sind bereits abgemeldet. Diese Emailadresse befindet sich nicht mehr in der Datenbank"
    return render(request, 'filme/newsletter_unsubscribe.html', { 'email': email, 'status': status })

def newsletter_render_today(request):
    '''render Ansicht für den Newsletter
    mit den events von heute'''
    nextevents = get_programm_query()
    hinweis = Inhaltsseite.objects.get(typen='1')
    if nextevents:
        datum = nextevents[0].termin.date() # hole Tag
        events = Event.objects.filter(event_online=True, termin__date = datum).order_by('termin')
    else: 
        events = nextevents # empty
        print('kein Film mehr im aktuellen Programm')
    return render(request, 'filme/newsletter_render_today.html', {'events': events, 'hinweis': hinweis })


def newsletter_render_hinweis(request):
    '''render Ansicht für den Newsletter
    mit dem Hinweis der Class Inhaltsseite'''
    # '1' = 'Hinweis_auf_Startseite'
    hinweis = Inhaltsseite.objects.get(typen='1')
    return render(request, 'filme/newsletter_render_hinweis.html', {'hinweis': hinweis })

@login_required
def sondernews_send(request, pk, email='@all'):
    '''sende Sondernewsletter
    <pk> des newsletters
    <email> für testmail oder @all
   '''
    logger.info("sondernews_send:  request.user  %s", request.user)
    typ = "Sondernewsletter"
    if email == '@all':
        sonder_newsletter = get_object_or_404(Sondernewsletter, pk=pk)
        sonder_newsletter.gesendet = datetime.datetime.now()
        sonder_newsletter.sender = request.user
        sonder_newsletter.save()
        logger.info("sondernews_send:  sonder_newsletter.gesendet  %s", sonder_newsletter.gesendet)

    newsletter = NewsletterSent.objects.create()              
    t = threading.Thread(
    target=newsletter.sent_newsletter,
        # args=('newsletter_render_today', "[Kino35] Das Programm für heute.", ), 
        args=('sondernewsletter_render', "[Kino35] Sondernewsletter!", pk, email ), 
        kwargs={})
    t.setDaemon(True)
    t.start()            
    return render(request, 'filme/newsletter_send.html',  {'start': newsletter.gestartet, 
                    'ende': newsletter.beendet,  'count': newsletter.anzahl, 'timediff': 'in der mail', 'key': 'via login', 'typ': 'Sondernewsletter' })


def newsletter_send(request, typ, key):
    '''sende Newsletter
    <typ> heute, das Programm von heute, falls es eines gibt
    <typ> hinweis, falls es einen gibt
    <typ> sondernewsletter, pk
    <key> aus privat_settings
    <pk> falls Sondernewsletter, um den richtigen zu versenden (default None)
    '''
    # Das Programm von heute
    if typ == 'heute':
        if key == HEUTE_KEY:
            nextevents = get_programm_query()
            if nextevents: # wenn ein event existiert
                datum = nextevents[0].termin.date() # hole den Tag des nächsten events
            else:
                datum = False
            # sende nur, wenn es heute einen event gibt
            if datetime.datetime.now().date() == datum: 
            # eine Woche im Voraus               
           # if datetime.datetime.now()+datetime.timedelta(days=7).date() == datum: 
                print('### newsletter send; heute:')

                newsletter = NewsletterSent.objects.create()              
                # newsletter.sent_newsletter('newsletter_render_today', "[Kino35] Das Programm für heute.")
                t = threading.Thread(
                    target=newsletter.sent_newsletter,
                    # args=('newsletter_render_today', "[Kino35] Das Programm für heute.", ), 
                    args=('newsletter_render_today', "[Kino35] heute läuft:", ), 
                    kwargs={})
                t.setDaemon(True)
                t.start()            
                return render(request, 'filme/newsletter_send.html',  {'start': newsletter.gestartet, 
                    'ende': newsletter.beendet,  'count': newsletter.anzahl, 'timediff': 'in der mail', 'key': True, 'typ': typ })

            else: #heute kein Event
                return render(request, 'filme/newsletter_send.html', {'key': 'heute kein Film, nix gesendet' })
        else:
            print('### key falsch, Programm heute nicht gesendet')
    
         # Sende den Hinweis der Startseite
    if typ == 'hinweis':
        print('### newsletter send; hinweis:')
        #überprüfe key 
        if key == HINWEIS_KEY:
            if (Inhaltsseite.objects.get(typen='1').anzeigen == True):
                newsletter = NewsletterSent.objects.create()
                # newsletter.sent_newsletter('newsletter_render_hinweis',"[Kino35] Hinweis")
                t = threading.Thread(
                    target=newsletter.sent_newsletter,
                    args=('newsletter_render_hinweis',"[Kino35] Hinweis", ),                         kwargs={})
                t.setDaemon(True)
                t.start()            
                return render(request, 'filme/newsletter_send.html',  {'start': newsletter.gestartet,
                     'ende': newsletter.beendet,  'count': newsletter.anzahl, 'timediff': 'in der mail', 'key': True, 'typ': typ })

            else: # Es gibt aktuell keinen _Hinweis
                    return render(request, 'filme/newsletter_send.html', {'key': 'heute kein Hinweis, nix gesendet' })
        else:
                print('### key falsch, hinweis nicht gesendet')           
    return render(request, 'filme/newsletter_send.html', {'key': False })
    
 

           
def event_publish(event):
    ''' Ein Filmevent geht online wenn
    - event_film_confirmed =True
    - film_komplett=True'''
    print('#### checke event ', event)
    print('event.event_film_confirmed ',event.event_film_confirmed,'event.film.film_komplett ',event.film.film_komplett)
    if event.event_film_confirmed  and event.film.film_komplett:
        event.event_online = True
        event.film.film_no_delete = True
        print('event.event_online ',event.event_online,'event.film.film_no_delete ',event.event_online)
        if not event.film.plakat:
            event.film.plakat = 'filme/defaults/plakatdummy-rot.png'
        event.film.save()
        event.save()
    return True

def get_programm_query():
    '''Programmfilter für index.html und Programmübersicht'''
    return Event.objects.filter(event_online=True,termin__gte=datetime.datetime.now()).order_by('termin')

def get_sidebar_query(delta):
    '''Programmfilter für den sidebar; zeige filme mit Abstand int(delta) in Tagen zur nächsten Veranstalltung'''
    # mydate: delta Tag nach der nächsten Veranstalltung (datetime)
    # 0 für Programm (der nächste Film, 1 Für Startseite <= 0 wird ja bereits angezeigt)
    relevant = []
    mydate = get_programm_query()
    try:
        mydate = mydate[0].termin + datetime.timedelta(days=delta)
        # alle Filme des nächsten Tages ab mitternacht
        mydate = mydate.replace(hour=0, minute=0, second=0)
    except IndexError as e: # keine filme da
        # print('Keine Filme für den Sidebar vorhanden: ', e)
        logger.info("def get_sidebar_query: %s", e)

        return relevant   
    # suche aus jeder kategorie den näachten event nach mydate
    for kategorie in Event.KATEGORIE_CHOICES:
        if Event.objects.filter(event_online=True,termin__gte=mydate, kategorie = kategorie[0]).count() > 0:
            nextobject = Event.objects.filter(event_online=True,termin__gte=mydate, kategorie = kategorie[0]).order_by('termin')[0]
            relevant.append( nextobject )
    # sortiere diese liste nach dem Datum
    relevant.sort(key=lambda x: x.termin)
    # return list of Event.objects
    return relevant

@login_required
def film_neu(request):
    '''neuen Film angelegen'''
    if request.method == "POST":
        form = FilmNeuForm(request.POST)
        if form.is_valid():
            film = form.save(commit=False)
            film.vorschlags_datum = datetime.datetime.now()
            film.save()
            return redirect( 'film_index' )
    else:
        form = FilmNeuForm()
    return render(request, 'filme/film_neu.html', {'form': form})

@login_required
def film_draft_sichten_list(request):
    '''Listenansicht aller neu angelegten Filme.
    Jeder Film ist mit 'film_draft_bewertung' verlinkt'''
    filme = Film.objects.filter(status = '1' ).order_by('vorschlags_datum')
    return render(request, 'filme/film_draft_list.html', {'filme': filme }) 

@login_required
def film_remove(request, pk):
    '''löscht den Film mit pk=pk    
    akzeptiert ?next=path für den redirect. ''' 
    film = get_object_or_404(Film, pk=pk)
    if film.film_no_delete == True:
        print(film.name, " ist löschgeschützt.")
    else:
        film.delete()
    next = request.GET.get('next', '/')
    return redirect(next)

def filmevent_detail(request, pk):
    '''details zum Filmevent
    aufruf mit event.pk '''
    event = get_object_or_404(Event, pk=pk) #stellt sicher, dass es pk gibt
    event = Event.objects.filter(pk=pk)#holt den event
    sidebar_events = get_sidebar_query(1)
    caler = 'filmevent_detail' # zur differenzeirung im tempale
    #film = get_object_or_404(Film, pk=event.film.pk)
    if request.method == "POST":
        return newsletter_form_snippet(request)
    else:
        form = NewsletterAboForm()
    #return render(request, 'filme/filmevent_detail.html', {'event': event, 'film': film }) 
    return render(request, 'filme/filmevent_detail.html', {'caler': caler, 'events': event, 'form': form, 'sidebar_events': sidebar_events})



@login_required
def film_status(request, pk, key):
    '''Ändert den status des Films
    akzeptiert ?next=path für den redirect.'''
    film = get_object_or_404(Film, pk=pk)
    try:
        film.status = key
    except:
        print('konnte status nicht setzen')
    film.save()
    next = request.GET.get('next', '/')
    return redirect(next)

@login_required
def film_draft_bewertung(request, pk):
    '''ein Vorauswahl treffen
        - bewerten
        - löschen
        - (für Programmauswahl markieren)
    akzeptiert ?next=path" für den redirect.
    path={{request.path}} leitet zur aufrufenden Seite zurück '''
    film = get_object_or_404(Film, pk=pk)
    if request.method == "POST":
        form = FilmBewertungForm(request.POST, request.FILES, instance=film)
        if form.is_valid():
            film = form.save(commit=False)
            film.interne_bewertung_ratio = film.set_ratio()
            film.save()
            next = request.GET.get('next', '/')
            return redirect(next)
    else:
        form = FilmBewertungForm(instance = film)
    return render(request, 'filme/film_draft_bewertung.html', {'form': form, 'film': film  })

@login_required
def film_draft_programmplanung_list(request):
    '''Aus den bewerteten Filmen die Auswahl für die Programmplanung treffen.
        Jeder Film ist mit 'film_draft_bewertung' verlinkt'''
    filme = Film.objects.filter(status = '2').order_by('name')
    return render(request, 'filme/film_draft_list.html', {'filme': filme })

@login_required
def film_archiv(request):
    '''Sammelbecken für Filme,
    welche keinen Termin haben
    Filme mit Termin finden sich 
    in der Chronik filmevent_archiv'''
    filme = Film.objects.filter(status = '4',event_film__isnull = True ).order_by('name')
    return render(request, 'filme/film_draft_list.html', {'filme': filme }) 



@login_required
def film_spielplanung_list(request, kat=0):
    '''Hier werden Vorführtermine mit den Filmen verbunden.
    Es werden alle zukünftigen Termine angezigt.
    Es können alle Filme 'film.status ='3' Programmplanung ausgewählt werden.
    Es kann ein neuer Termin hinzugefügt werden.
    '''
    kategorieauswahl=kat # 0 sind alle (default) wird über url gesteuert
    SpielplanFormSet = modelformset_factory(Event, form=SpielplanForm)
    events_next = get_spielplanung_query(kategorieauswahl)
    set_zeit(events_next)
    filme = Film.objects.filter(status = '3' )
    if request.method == 'POST':
        formset = SpielplanFormSet(request.POST, queryset = events_next)
        if formset.is_valid():
            events = formset.save(commit=False)
            set_termin(events) # mache datetime  und korrigiere event_online falls nötig
            # setze online
            formset.save()
        events_next = get_spielplanung_query(kategorieauswahl)
        formset = SpielplanFormSet(queryset = events_next)
        return redirect('film_spielplan_list')
    else:
        formset = SpielplanFormSet(queryset = events_next)
    return render(request, 'filme/film_spielplanung.html', {'formset': formset, 'filme': filme })

def get_spielplanung_query(kategorieauswahl):
    '''Event filter für film_spielplanung_list, da er
    dort zweifach verwendet wird'''
    print("kategorieauswahl =", kategorieauswahl)
    if kategorieauswahl != 0:
        return Event.objects.filter(termin__gte=datetime.datetime.now() ).filter(kategorie=kategorieauswahl).order_by('termin')[:100]
    else: # alle kategorien
        return Event.objects.filter(termin__gte=datetime.datetime.now() ).order_by('termin')[:100]

def set_zeit(events):
    '''Schreibt 'time' aus 'termin' in 'zeit'.'''
    for idx, i in enumerate(events):
        events[idx].zeit = events[idx].termin.time()
        events[idx].save()

def set_termin(events):
    '''Schreibt 'zeit' in 'time' von 'termin'.
    und lösche online wenn ein event keinen Film mehr hat
    '''
    for idx, i in enumerate(events):
        # schreibe die Urhzeit in Datetime
        events[idx].termin = datetime.datetime.combine(events[idx].termin, events[idx].zeit)
        # setze event_online auf False, falls ein Film aus dem Programm gelöscht wurde
        if (events[idx].film is None):
            events[idx].event_online = False
            # dadurch ist vielleicht auch die Verleihbestätigung nicht mehr da
            events[idx].event_film_confirmed = False
        events[idx].save()

@login_required
def event_new(request):
    '''Hier werden Serientermine angelegt'''
    if request.method == "POST":
        form = EventNeuForm(request.POST)
        if form.is_valid():
            wdh = int(request.POST['wdh'])
            zeit = request.POST['zeit']
            time_object = datetime.datetime.strptime(zeit, '%H:%M').time()
            event = form.save(commit=False)
            termin = datetime.datetime.combine(event.termin, time_object)
            event.termin = termin
            event.save()
            # lege Wiederholungen an.
            for x in range(1, wdh):
                termin = termin + datetime.timedelta(days=7)
                next = Event(termin = termin, kategorie = event.kategorie )
                next.save()
            return redirect('film_spielplanung_list')
    else:
        form = EventNeuForm()
    return render(request, 'filme/event_new.html', {'form': form})


@login_required
def film_spielplan_list(request):
    '''Dort erscheinen alle Hauptfilme, welchen in der Programmplanung
    ein Termin zugeordnet wurde.'''
    events = Event.objects.filter(termin__gte = datetime.datetime.now()).order_by('termin')
    return render(request, 'filme/film_spielplan_list.html', { 'events': events }) 

@login_required
def filmevent_archiv(request):
    '''Alle gezeigten Filme'''
    events = Event.objects.filter(termin__lte = datetime.datetime.now()).order_by('-termin')
    # lösche events in der Vergangenheit ohne film
    for event in events:
        if not event.film:
            print('## lösche vergangenen event ohne Film: ', event)
            event.delete()
            events = Event.objects.filter(termin__lte = datetime.datetime.now()).order_by('-termin')
    return render(request, 'filme/filmevent_archiv.html', { 'events': events }) 

def filmevent_openarchiv(request):
    '''Alle gezeigten Filme für alle'''
    events = Event.objects.filter(termin__lte = datetime.datetime.now()).order_by('-termin')
    # lösche events in der Vergangenheit ohne film
    for event in events:
        if not event.film:
            print('## lösche vergangenen event ohne Film: ', event)
            event.delete()
            events = Event.objects.filter(termin__lte = datetime.datetime.now()).order_by('-termin')
    return render(request, 'filme/filmevent_archiv.html', { 'events': events }) 

@login_required
def confirm_eventfilm(request, pk):
    '''Film wird für den Termin bestätigt.
    akzeptiert ?next=path für den redirect.'''
    event = get_object_or_404(Event, pk=pk)
    event.event_film_confirmed = True
    event.save()
    event_publish(event) # check in der funktion
    next = request.GET.get('next', '/')
    return redirect(next)

@login_required
def film_detail_edit(request, pk):
    ''' Hier können alle Filminformationen bearbeitet werden'''
    film = get_object_or_404(Film, pk=pk)
    if request.method == "POST":
        form = FilmForm(request.POST, request.FILES, instance=film)
        if form.is_valid():
            film = form.save(commit=False)
            film.save()
            if ('film_komplett' in form.changed_data and film.film_komplett):
                # changed true
                # lasse alle zukünftigen events zum film checken
                for event in film.event_film.all().filter(termin__gte=datetime.datetime.now()):
                    event_publish(event)
            next = request.GET.get('next', '/')
            return redirect(next, pk=film.pk)
            #return redirect('film_detail', pk=film.pk )
    else:
        form = FilmForm(instance=film)
    return render(request, 'filme/film_detail_edit.html', {'form': form, 'film': film })


@login_required
def sondernewsletter_list(request):
    '''Übersicht der Sondernewsletter.'''
    newsletters = Sondernewsletter.objects.order_by('-erstellt')[:20]
    return render(request, 'filme/newsletter_sondernewsletter_list.html', { 'newsletters': newsletters })     

@login_required
def sondernewsletter_neu(request):
    '''neuen Sondernewsletter angelegen'''
    if request.method == "POST":
        form = NewsletterForm(request.POST)
        if form.is_valid():
            newsletter = form.save(commit=False)
            newsletter.save()
            print('Newsletter angelegt. pk',newsletter.pk)
            return redirect( 'sondernewsletter_edit', pk=newsletter.pk )
        else:
            print('not valid')
    else:
        form = NewsletterForm()
    return render(request, 'filme/newsletter_sondernewsletter_neu.html', {'form': form})

@login_required
def sondernewsletter_delete(request, pk):
    '''löscht den sondernewsletter_delete mit pk=pk    
    sofern noch nicht versendet ''' 
    newsletter = get_object_or_404(Sondernewsletter, pk=pk)
    if newsletter.gesendet:
        print(newsletter.titel, " ist löschgeschützt.")
    else:
        newsletter.delete()
    return redirect('sondernewsletter_list')



@login_required
def sondernewsletter_edit(request, pk):
    '''Sondernewsletter überarbeiten und versenden.'''
    logger.debug("sondernewsletter_edit: start")
    newsletter = get_object_or_404(Sondernewsletter, pk=pk)
    if request.method == "POST":
        form = NewsletterForm(request.POST, request.FILES, instance=newsletter )
        if form.is_valid():
            newsletter = form.save(commit=False)
            if newsletter.gesendet:
                newsletter.pk = None # erstelle Kopie
                newsletter.gesendet = None
            newsletter.save()
            return redirect( 'sondernewsletter_edit', pk = newsletter.pk )
    else:
        form = NewsletterForm(instance=newsletter)
    logger.debug("sondernewsletter_edit:  request.user  %s newsletter.bild_thumb.url %s", request.user, newsletter.bild_thumb.url)
    return render(request, 'filme/newsletter_sondernewsletter_edit.html', {'user': request.user, 'newsletter': newsletter, 'form': form})  

def sondernewsletter_render(request, pk):
    '''Sondernewsletter gerendert für versand und check.'''
    newsletter = get_object_or_404(Sondernewsletter, pk=pk)
    return render(request, 'filme/newsletter_render_sondernewsletter.html', {'newsletter': newsletter})  



def film_detail(request, pk):
    '''Die Detailansicht des Films'''
    film = get_object_or_404(Film, pk=pk)
    sidebar_events = get_sidebar_query(0)

    if request.method == "POST":
        form = NewsletterAboForm(request.POST)
        if form.is_valid():
            abo = form.save(commit=False)
            abo.save()
            flag = 'neu'
            user = NewsletterAbonnent.objects.get(email = abo.email)
            user.sent_opt_in()
            return redirect( 'newsletter_abo_feedback', flag = flag)
        else:
            email = request.POST['email']
            flag="error"
            user = NewsletterAbonnent.objects.get(email = email)
            if user.opt_in:
                flag="OK"
            else:
                flag="wartend"
                user.sent_opt_in()
            return redirect( 'newsletter_abo_feedback', flag = flag)
    else:
        form = NewsletterAboForm()

    return render(request, 'filme/film_detail.html', {'film': film, 'form': form, 'sidebar_events': sidebar_events })

def filmevent_detail_edit(request, pk):
    '''Einen Event bearbeiten, Text, Dienste, Film bestätigen'''
    event = get_object_or_404(Event, pk=pk)
    if request.method == "POST":
        form = EventDetailForm(request.POST, instance=event)
        if form.is_valid():
            event = form.save(commit=False)
            got = ZeitStempel.objects.get(user = request.user ).zeit
            debugmessage = 'event.last_change', event.last_change, ' > ', 'eigener Abruf:', got         
            messages.debug(request, debugmessage)  
            # if last_change > got <=  Änderung seit Aufruf des Formulars
            if event.last_change > got:
                # give error and reload
                messages.error(request, 'Mist, die Datenbank wurde in der Zwischenzeit geändert. Hier sind die aktuellen Daten. Bitte nochmal!')              
                # setze neuen zeitstempel
                request.user.zeitstempel.zeit = datetime.datetime.now()
                request.user.zeitstempel.save()
                event.refresh_from_db()
                form = EventDetailForm(instance=event)
            else:
                # last_change is now
                event.last_change = datetime.datetime.now()
                event.save()
                messages.success(request, 'Änderungen in Filmevent gespeichert!') 

                event_publish(event)
                next = request.GET.get('next', '/')
                return redirect(next)
    else:
        # set user get
        request.user.zeitstempel.zeit = datetime.datetime.now()
        request.user.zeitstempel.save()
        form = EventDetailForm(instance=event)
    return render(request, 'filme/filmevent_detail_edit.html', {'form': form, 'event': event })


@login_required
def filmevent_dienste(request, pk):
    '''Hier werden die Dienste und der interne Text zum Filmevent bearbeitet'''
    event = get_object_or_404(Event, pk=pk)
    if request.method == "POST":
        form = EventDiensteForm(request.POST, instance=event)
        if form.is_valid():
            event = form.save(commit=False)
            got = ZeitStempel.objects.get(user = request.user ).zeit
            debugmessage = 'event.last_change', event.last_change, ' > ', 'eigener Abruf:', got         
            messages.debug(request, debugmessage)  
            # if last_change > got <=  Änderung seit Aufruf des Formulars
            if event.last_change > got:
                # give error and reload
                messages.error(request, 'Mist, die Datenbank wurde in der Zwischenzeit geändert. Hier sind die aktuellen Daten. Bitte nochmal!')              
                # setze neuen zeitstempel
                request.user.zeitstempel.zeit = datetime.datetime.now()
                request.user.zeitstempel.save()
                event.refresh_from_db()
                form = EventDetailForm(instance=event)
            else:
                # last_change is now
                event.last_change = datetime.datetime.now()
                event.save()
                messages.success(request, 'Änderungen in Filmevent gespeichert!') 
                return redirect('/')
    else:
        # setze zeitstempel
        request.user.zeitstempel.zeit = datetime.datetime.now()
        request.user.zeitstempel.save()
        form = EventDetailForm(instance=event)
    return render(request, 'filme/filmevent_dienste.html', {'form': form, 'event': event})




def film_impressum(request):
    inhalt = Inhaltsseite.objects.filter(typen = 2)
    inhalt = inhalt[0]  
    return render(request, 'filme/inhaltsseite.html', {'inhalt': inhalt })  

def film_datenschutzhinweis(request):
    inhalt = Inhaltsseite.objects.filter(typen = 3)
    inhalt = inhalt[0]
    return render(request, 'filme/inhaltsseite.html', {'inhalt': inhalt })  

def film_ueber_uns(request):
    inhalt = Inhaltsseite.objects.filter(typen = 4)
    inhalt = inhalt[0]
    return render(request, 'filme/inhaltsseite.html', {'inhalt': inhalt }) 

def film_anfahrt(request):
    inhalt = Inhaltsseite.objects.filter(typen = 5)
    inhalt = inhalt[0]
    return render(request, 'filme/inhaltsseite.html', {'inhalt': inhalt }) 

def import_drupal(request):
    url = 'http://35kino.de/service/flyer'
    html_doc = requests.get(url).text
    soup = BeautifulSoup(html_doc, 'html.parser')
    # text = soup.find('div', attrs={'class' : 'TITEL'}).string
    #for titel in soup.find_all('div', attrs={'class' : 'TITEL'}) :
    #        print('Titel: ', titel.string )
    for view in soup.find_all('div', attrs={'class' : 'views-row-1'}):
        print('# view:', view)
        event='bla'
        name = (view.find('div', attrs={'class' : 'TITEL'}).string)
        plakat = False
        plakat = view.find('div', attrs={'class' : 'PLAKAT'})
        ## False falls kein Plakat
        if True:
            plakat_url = str(plakat.find('a').get('href'))
        datum = view.find('div', attrs={'class' : 'DATUM'}).string
        datum = parser.parse(datum) # mache datetime object aus string
        # der termin für event, datum wird nun nciht mehr gebraucht
        termin = datum.replace(tzinfo=None)
        land = view.find('div', attrs={'class' : 'LAND'}).string
        jahr = view.find('div', attrs={'class' : 'JAHR'}).string
        dauer = view.find('div', attrs={'class' : 'DAUER'}).string
        fsk = (view.find('div', attrs={'class' : 'FSK'}).string)
        genre = view.find('div', attrs={'class' : 'GENRE'}).string
        regie = view.find('div', attrs={'class' : 'REGIE'}).string
        darsteller = view.find('div', attrs={'class' : 'DARSTELLER'}).string
        # text = view.find('div', attrs={'class' : 'TEXT'}).get_text()

        # erstelle Film oder hole ihn aus db
        film, created = Film.objects.get_or_create(name=name)
        if created:
            print(film, ' erstellt')
            film.film_komplett=True
            film.film_no_delete=False
            film.film_no_delete=True
            film.vorschlags_datum=termin
            ### falls kein Plakat False
            if True:
                plakat_name = plakat_url.split("/")
                plakat_name = plakat_name[len(plakat_name)-1]
                response = urlopen(plakat_url)  
                io = BytesIO(response.read())  
                film.plakat.save(plakat_name, File(io))
            film.director = regie
            if jahr:
                film.datePublished = int(jahr)
            film.actors = darsteller
            film.countryOfOrigin = land
            if dauer:
                film.duration = int(dauer)
            film.genre = genre
            if fsk:
                if (fsk == 'null') or (fsk == 'ab 0'):
                    film.fsk = 'fsk0'
                if (fsk == 'FSK 6') or (fsk == 'ab 6'):
                    film.fsk = 'fsk6'
                if (fsk == 'FSK 12') or (fsk == 'ab 12'):
                    film.fsk = 'fsk12'
                if (fsk == 'FSK 16') or (fsk == 'ab 16'):
                    film.fsk = 'fsk16'
                if (fsk == 'FSK 18') or (fsk == 'ab 18'):
                    film.fsk = 'fsk18'
            # film.description = text
            film.status = '4'
            film.save()
        else:
            print(film, ' war schon in DB')            
        print('TERMIN', termin, film)
        # erstelle Event oder hole ihn aus db
        event, created = Event.objects.get_or_create(termin=termin, film=film)
        if created:
            print('    neuer event am ', event)
            event.event_online = True
            event.event_film_confirmed = True
            event.text_intern ="von der alten Website importiert"
            # location_address = "Langebrückenstraße 14, 36037 Fulda"
            event.save()
        else:
            print('    hatte schon einen Event am ', event)

    return render(request, 'filme/import_drupal.html', {'filmevents': event })

def import_newsletter_abos():
    print('################ file')
    file_ = open(os.path.join(settings.BASE_DIR, 'newsletter'))
    print(file_)
    # lade aus Datei newsletter
    emails = [line.rstrip('\n') for line in file_]
    emails = emails[0].split('|')
    # # loope durch Komasepariert
    for email in emails:
       # print('mail:', email)
    #     # lege def import_
        nextuser = NewsletterAbonnent.objects.create()
        nextuser.email = email
        opt_in = True
        nextuser.salz = BaseUserManager().make_random_password() # erhält passwort
        nextuser.save()
    print('##############')


def import_users():
    print('################ file')
    file_ = open(os.path.join(settings.BASE_DIR, 'users'))
    print(file_)
    # lade aus Datei newsletter
    emails = [line.rstrip('\n') for line in file_]
    #emails = emails[0].split(',')
    # # loope durch Komasepariert
    for email in emails:
        email = email.split('|')
        print(email[1], email[2])
        user = get_user_model().objects.create_user(
            username= email[1] ,
            email= email[2],
            password=BaseUserManager().make_random_password(),
            is_staff = 1,
            is_active = 1)
    print('##############')



#             film.vorschlags_datum = datetime.datetime.now()


# https://stackoverflow.com/questions/1393202/django-add-image-in-an-imagefield-from-image-url          


# def event_detail(request, pk):
#     event = get_object_or_404(Event, pk=pk)
#     return render(request, 'filme/event_detail.html', {'event': event})



# def add_comment_to_film(request, pk):
#     film = get_object_or_404(Film, pk=pk)
#     if request.method == "POST":
#         form = CommentForm(request.POST)
#         if form.is_valid():
#             comment = form.save(commit=False)
#             comment.film = film
#             comment.save()
#             return redirect('film_detail', pk=film.pk)
#     else:
#         form = CommentForm()
#     return render(request, 'filme/add_comment_to_film.html', {'form': form,'film': film})

# @login_required
# def comment_approve(request, pk):
#     comment = get_object_or_404(Comment, pk=pk)
#     comment.approve()
#     return redirect('film_detail', pk=comment.film.pk)

# @login_required
# def comment_remove(request, pk):
#     comment = get_object_or_404(Comment, pk=pk)
#     comment.delete()
#     return redirect('film_detail', pk=comment.film.pk)    

