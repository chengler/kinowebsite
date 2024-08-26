from django.contrib.auth.models import Group

from urllib import request
from django.conf import settings
from django.db import models

from django.utils import timezone
from django.core.files.uploadedfile import InMemoryUploadedFile
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from django.core.validators import MaxValueValidator
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.safestring import mark_safe
import datetime
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import get_template
import requests
import time
import html2text
from django.db.models import Q

# from django.shortcuts import render1
from django.urls import reverse
from django.core import mail
import logging
from logging import FileHandler
from mysite.privat_settings import DEFAULT_DOMAIN
from mysite.newsletter_keys import *


logger = logging.getLogger(__name__)
# custom user für das nächste Projekt
# https://learndjango.com/tutorials/django-best-practices-referencing-user-model


#  limit_choices_to={'status': '3' }
def limit_film_choices():
    datum = str(datetime.datetime.now())
    result = (
        Q(status="3")
        | Q(event_film__termin__gte=datum)
        | Q(event_ersatz__termin__gte=datum)
    )
    # result = { 'status': 3 }
    # alle filme mit film.status : 3
    # alle Filme, auf die ein zukünftiger Termin verweist
    # related_name='event_film'
    # related_name='event_ersatz
    # print("###result",result)
    logger.debug("def limit_film_choices(): %s", result)
    return result


class Flyer(models.Model):
    """zum speicher und anzeigen von Programmflyern.
    admin.py class FlyerAdmin(admin.ModelAdmin):
    bearbeite unter admin/filme/flyer/
    Html: flyer_snippet.html"""

    def dateiname(instance, filename):
        """Legt den Dateipfad fest
        media/flyer/<kino>_<yy-mm>.pdf"""
        datum = instance.bisZum.strftime("%y%m")
        pfad = "flyer/" + instance.prefix + "_" + datum + ".pdf"
        logger.debug("*** class Flyer: def dateiname: PFAD: %s ", pfad)
        return pfad

    @staticmethod
    def get_flyer_query():
        """ladet alle noch nicht abgelaufenen Flyer in 'aktuelle_flyers'
        Bezugspumkt ist heute und das date Feld bisZum"""
        aktuelle_flyers = Flyer.objects.filter(
            bisZum__gte=datetime.date.today()
        )  # .order_by('bisZum')
        logger.debug(
            "*** views: def get_flyer_query: aktuelle_flyers: %s ", aktuelle_flyers
        )
        return aktuelle_flyers

    bisZum = models.DateField(
        auto_now=False, blank=False
    )  # Flyer wird angezeigt bis zum
    bisZum.help_text = "Bis wann hat dieser Flyer gültigkeit? Bis zu diesem Tag wfInhaltsird der Flyer angezeigt werden. \n Jahr (yy) und Monat (mm) wird für den Pfad zum Flyer verwendet"
    prefix = models.CharField(
        max_length=8, default="kino", blank=False
    )  # um mehrere Flyer wie Kino, Banzai anzuzeigen
    prefix.help_text = "Handle with care! Das Prefix wird für den Pfad zum Flyer verwendet. default = kino</br> Damit können Flyer unterschieden werden, welche im gleichen Monat enden, oder anders beginnen sollen als kino z.B. mufi, banzai "
    anzeigename = models.CharField(
        max_length=32, blank=False
    )  # Name wie Kino Oktober/November
    anzeigename.help_text = (
        "Dieser Name wird auf der Webseite angezigt. z.B. Kino Oktober/November"
    )
    flyer = models.FileField(upload_to=dateiname)
    flyer.help_text = (
        "Der Pfad zur Datei ist: " + DEFAULT_DOMAIN + "/media/flyer/prefix_yy-mm.pdf"
    )


class Film(models.Model):
    # author = models.ForeignKey(settings.AUTH_USER_MODEL, default='unbekannt', on_delete=models.SET_DEFAULT)
    # https://schema.org/Movie
    name = models.CharField(max_length=128, unique=True)  # Name, Titel
    trailer = models.URLField(max_length=128, null=True, blank=True)  # trailer zum film
    website = models.URLField(
        max_length=128, null=True, blank=True
    )  # website zu Film oder kritik
    plakat = models.ImageField(
        upload_to="filme/plakate/",
        blank=True,
        default="filme/defaults/plakatdummy-rot.png",
    )

    plakat_minithumb = ImageSpecField(
        source="plakat",
        processors=[ResizeToFill(50, 70)],
        format="JPEG",
        options={"quality": 80},
    )

    plakat_thumbnail = ImageSpecField(
        source="plakat",
        processors=[ResizeToFill(150, 210)],
        format="JPEG",
        options={"quality": 90},
    )
    plakat_klein = ImageSpecField(
        source="plakat",
        processors=[ResizeToFill(250, 350)],
        format="JPEG",
        options={"quality": 90},
    )
    plakat_gross = ImageSpecField(
        source="plakat",
        processors=[ResizeToFill(500, 700)],
        format="JPEG",
        options={"quality": 90},
    )
    director = models.CharField(max_length=64, null=True, blank=True)  # Regie
    datePublished = models.PositiveIntegerField(
        validators=[MaxValueValidator(3000)], blank=True, null=True
    )  # copyrightYear
    actors = models.CharField(
        max_length=512,
        null=True,
        blank=True,
    )  # Schauspieler
    countryOfOrigin = models.CharField(
        max_length=128,
        null=True,
        blank=True,
    )
    duration = models.PositiveIntegerField(
        null=True, blank=True, validators=[MaxValueValidator(1000)]
    )  # Spieldauer in min
    genre = models.CharField(
        max_length=64,
        null=True,
        blank=True,
    )
    FSK_CHOICES = [
        ("fsk0", "FSK 0"),
        ("fsk6", "FSK 6"),
        ("fsk12", "FSK 12"),
        ("fsk16", "FSK 16"),
        ("fsk 18", "FSK 18"),
    ]
    fsk = models.CharField(choices=FSK_CHOICES, null=True, blank=True, max_length=16)
    hinweis = models.TextField(
        default="", blank=True
    )  # spezeiller Hinweis zum Film OmU,Kooperationspartner ...
    hinweis.help_text = "hinweis: Ein spezieller Hinweis zu Film, aber nicht die Filmbeschreibung. Meist leer. html möglich. gehört eigentlich eher zur veranstalltung und wird bald ersetzt."
    description = models.TextField(default="", blank=True)  # Filmbeschreibung
    description.help_text = "description: Die eigentliche Filmbeschreibung"
    vorschlags_datum = models.DateTimeField(
        default=timezone.now, blank=True
    )  # wann wurde der Film das erste mal vorgeschlagen/erstellt
    interner_kommentar = models.TextField(
        blank=True, null=True
    )  # Feedback der Programmplanungsgruppe
    interne_bewertung_zahl = models.SmallIntegerField(
        null=True, default=0, blank=True
    )  # Feedback Programmplanungsgruppe <= wieviele dafür
    interne_bewerter_zahl = models.SmallIntegerField(
        null=True, default=0, blank=True
    )  # Feedback Programmplanungsgruppe <= wie viele nehmen Teil
    interne_bewertung_ratio = models.SmallIntegerField(
        null=True, default=0, blank=True
    )  # Feedback Ratio <= bewertung * 10 / bewerter

    film_komplett = models.BooleanField(
        default=False, blank=True
    )  # bereit zur veröffentlichung
    film_no_delete = models.BooleanField(
        default=False, blank=True
    )  # veröffentlicht, nicht mehr löschen
    STATUS_COICES = [
        ("1", "Sichtung"),
        ("2", "Vorauswahl"),
        ("3", "Programmplanung"),
        ("4", "Archiv"),
    ]
    status = models.CharField(max_length=16, choices=STATUS_COICES, default="1")

    #  in_bearbeitung = models.BooleanField( default = True)

    def set_ratio(self):
        """berechne das Bewertungsratio 10 alle dafür, 0 keiner dafür"""
        try:
            self.interne_bewertung_ratio = round(
                (((self.interne_bewertung_zahl * 100) / self.interne_bewerter_zahl))
            )
            if self.interne_bewertung_ratio > 100:
                self.interne_bewertung_ratio = 0

            print("** interne_bewertung_ratio", self.interne_bewertung_ratio)
            print((((self.interne_bewertung_zahl * 10) / self.interne_bewerter_zahl)))
            logger.debug("def set_ratio(self):", self.interne_bewerter_zahl)

        except (ValueError, TypeError, ZeroDivisionError):
            self.interne_bewertung_ratio = 0
            print("Runden fehlgeschlagen")
            logger.warning("Runden fehlgeschlagen")

        return self.interne_bewertung_ratio

    def display_description(self):
        """zeigt den Text/description mit HTML Tags an, es sei denn, <script> wird verwendet"""
        if "<script" in self.description:
            return self.description
        return mark_safe(self.description)

    def display_hinweis(self):
        """zeigt den 'hinweis' zum Film mit HTML Tags an, es sei denn, <script> wird verwendet"""
        if "<script" in self.hinweis:
            return self.hinweis
        return mark_safe(self.hinweis)

    def fsk_verbose(self):
        return dict(Film.FSK_CHOICES)[self.fsk]

    def __str__(self):
        return self.name


# ergänze das user model um einen Zeitstempel
class ZeitStempel(models.Model):
    # user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="zeitstempel"
    )
    zeit = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.zeit.strftime("%Y-%m-%d %H:%M")


# neuer User => neuer Zeitstempel
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        ZeitStempel.objects.create(user=instance)


# für alte nutzer ohne zeitstempel
# nur eine übergangslösung, bis jeder einen hat
# neue user erhalten klasse  beim anlegen
# hier beim login
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if not ZeitStempel.objects.filter(user=instance):
        ZeitStempel.objects.create(user=instance)
        instance.zeitstempel.save()


class Event(models.Model):
    film = models.ForeignKey(
        "filme.Film",
        on_delete=models.CASCADE,
        related_query_name="event_film",
        related_name="event_film",
        blank=True,
        null=True,
        limit_choices_to=limit_film_choices,
    )
    ersatzfilm = models.ForeignKey(
        "filme.Film",
        on_delete=models.SET_NULL,
        related_query_name="event_ersatz",
        related_name="event_ersatz",
        blank=True,
        null=True,
        limit_choices_to=limit_film_choices,
    )
    termin = models.DateTimeField(auto_now=False, null=True)  # Termin der Vorführung
    zeit = models.TimeField(auto_now=False, null=True)  # dummy
    text_intern = models.TextField(blank=True, default="")  # intern zur Veranstalltung
    text_extern = models.TextField(
        blank=True, default=""
    )  # besonderes wie Regiseur anwesend
    location_name = models.TextField(
        default="Kino35", blank=True, max_length=64
    )  # Kino35
    location_address = models.TextField(
        default="Ohmstr. 18-20 36037 Fulda", blank=True, max_length=128
    )  # kann im Adminpannel geändert werden
    KATEGORIE_CHOICES = [
        ("1", "Freitagsfilm"),
        ("2", "KinderKino"),
        ("3", "Sonderveranstaltung"),
        ("4", "Lesung"),
        ("5", "Für die Ohren"),
        ("6", "Autokino"),
        ("7", "OpenAir"),
        ("8", "FIF"),
        ("9", "DokuDonnerstag"),
        ("10", "MuFi"),
        ("11", "BIPoC"),
        ("12", "Kino, Kaffee & Croissant"),
        ("13", "BANZAI!"),
        ("14", "Nachhaltigkeitsteam"),
        ("15", "Kurzfilmtag"),
        ("16", "Überraschungsfilm"),
        ("17", "Theater"),
    ]
    kategorie = models.CharField(
        max_length=16, choices=KATEGORIE_CHOICES, null=True, blank=True
    )

    event_online = models.BooleanField(
        default=False, blank=True
    )  # event confirmd und film komplett
    vorverkauf = models.BooleanField(default=False, blank=True)
    theke1 = models.CharField(max_length=32, default="", blank=True)
    theke2 = models.CharField(max_length=32, default="", blank=True)
    kasse = models.CharField(max_length=32, default="", blank=True)
    vorfuehrer = models.CharField(max_length=32, default="", blank=True)
    last_change = models.DateTimeField(auto_now=True)  # letzte Änderung der Dienste
    event_film_confirmed = models.BooleanField(
        default=False, blank=True
    )  # vorführrechte OK

    def display_text_extern(self):
        """zeigt den 'hinweis' zum event mit HTML Tags an, es sei denn, <script> wird verwendet"""
        if "<script" in self.text_extern:
            return self.text_extern
        return mark_safe(self.text_extern)

    def __str__(self):
        return self.termin.strftime("%Y-%m-%d %H:%M")

    # https://stackoverflow.com/questions/6558535/find-the-date-for-the-first-monday-after-a-given-a-date#6558571
    @staticmethod
    def next_day(given_date, weekday):
        """given date = datetime.date(2018, 4, 15)
        weekday = 1 für Montag .5..  Sonntag
        returns  nächster Wochentag in datetime => (15.4 - 21.4)
        """
        day_shift = (weekday - given_date.isoweekday()) % 7
        return given_date + datetime.timedelta(days=day_shift)


class Rollendoku(models.Model):
    """Dokumentationsseite für eine jeweilige Rolle wie z.B. admin
    Die Auswahl erfolgt dynamisch"""

    def get_Rollen():
        # [ ('1', 'admin' ), ...]
        gruppen = {group for group in Group.objects.all()}
        logger.debug("class Rollendoku Gruppen %s ", gruppen)
        gruppenlist = []
        for gr in gruppen:
            gruppenlist.append(tuple([str(gr.pk), gr.name]))
        logger.debug("Rollen Group.objects %s ", gruppenlist)
        return gruppenlist

    name = models.CharField(max_length=64)
    name.help_text = "Überschrift der Seite"
    text = models.TextField(blank=True, null=True)
    text.help_text = "Inhalt diser Seite"
    anzeigen = models.BooleanField(default=True)
    anzeigen.help_text = "Soll die Seite angezeigt werden?"
    ROLLEN_CHOICES = get_Rollen()
    group_id = models.CharField(null=True, max_length=150, choices=ROLLEN_CHOICES)
    group_id.help_text = "hier wird die id der Group gespeichert. angezeigt wird üblicherweise der Text z.B. admin"

    bild = models.ImageField(upload_to="filme/plakate/", blank=True, null=True)
    bild_klein = ImageSpecField(
        source="bild",
        processors=[ResizeToFill(320, 240)],
        format="JPEG",
        options={"quality": 90},
    )
    bild_gross = ImageSpecField(
        source="bild",
        processors=[ResizeToFill(640, 480)],
        format="JPEG",
        options={"quality": 90},
    )
    # def __str__(self):
    #     '''Ausgabe des Objektes ist der Rollenname wie admin'''
    #     return self.get_rolle_display()


class Inhaltsseite(models.Model):
    name = models.CharField(max_length=32, null=True, unique=True)
    text = models.TextField(blank=True, null=True)
    anzeigen = models.BooleanField(default=True)
    TYPEN_CHOICES = [
        ("1", "Hinweis_auf_Startseite"),
        ("2", "Impressum"),
        ("3", "Datenschutzhinweis"),
        ("4", "Über_uns"),
        ("5", "Anfahrt"),
        ("6", "MuFi"),
    ]
    typen = models.CharField(max_length=16, choices=TYPEN_CHOICES, unique=True)
    bild = models.ImageField(upload_to="filme/plakate/", blank=True, null=True)
    bild_klein = ImageSpecField(
        source="bild",
        processors=[ResizeToFill(320, 240)],
        format="JPEG",
        options={"quality": 90},
    )
    bild_gross = ImageSpecField(
        source="bild",
        processors=[ResizeToFill(640, 480)],
        format="JPEG",
        options={"quality": 90},
    )

    def __str__(self):
        return self.name


class Comment(models.Model):
    film = models.ForeignKey(
        "filme.Film", on_delete=models.CASCADE, related_name="comments"
    )
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    kommentar = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text


class NewsletterAbonnent(models.Model):
    email = models.EmailField(unique=True)
    beantragt = models.DateTimeField(
        auto_now_add=True
    )  # Datum um Karteileichen zu löschen
    opt_in = models.BooleanField(blank=True, default=False)
    salz = models.CharField(max_length=15, default=False)

    def sent_opt_in(self):
        """versendet Email zum opt_in"""
        logger.debug(
            "def sent_opt_in:  EMAIL_HOST_USER %s DEFAULT_FROM_EMAIL %s",
            EMAIL_HOST_USER,
            DEFAULT_FROM_EMAIL,
        )

        html_body = get_template("filme/newsletter_opt_in_email.html").render()
        change = (
            settings.DEFAULT_DOMAIN
            + "/newsletter/opt_in/"
            + self.email
            + "/"
            + self.salz
        )
        html_body = html_body.replace("#changeme#", change)
        text_maker = html2text.HTML2Text()
        text_maker.ignore_images = True
        text_body = text_maker.handle(html_body)
        subject = "Newsletterabo für's Kino35 bestätigen"
        #  from_email = EMAIL_HOST_USER
        from_email = DEFAULT_FROM_EMAIL
        to_email = self.email
        message = EmailMultiAlternatives(
            subject=subject, body=text_body, from_email=from_email, to=[to_email]
        )
        message.attach_alternative(html_body, "text/html")
        message.send()

    def empfange_opt_in(self, salz):
        """verarbeite opt_in Rückmeldung"""
        if self.salz == salz:  # überprüfe ob Absender auch das richtige Salz hatte
            if self.opt_in:
                status = "Diese Adresse wurde bereits erfolgreich bestätigt."
            else:
                self.opt_in = True
                status = (
                    "Diese Adresse wurde erfolgreich bestätigt. Herzlich Willkommen!"
                )
                self.save()
        else:
            status = "Email und Sicherheitscode passen nicht zusammen. Bestätigung gescheitert! Bitte kontaktieren Sie uns"
        return status

    def unsubscribe(self, salz):
        """verarbeite unsubscribe"""
        if self.salz == salz:  # überprüfe ob Absender auch das richtige Salz hatte
            status = "Ihr Abo wurde aus der Datenbank entfernt."
            self.delete()
        else:
            status = "Email und Sicherheitscode passen nicht zusammen. Löschung gescheitert! Bitte kontaktieren Sie uns"
        return status

    def __str__(self):
        return self.email


class NewsletterSent(models.Model):
    gestartet = models.DateTimeField(auto_now_add=True)
    beendet = models.DateTimeField(null=True)
    anzahl = models.PositiveSmallIntegerField(default=0)

    def sent_newsletter(self, view_name, subject="[Kino35]", pk=None, email="@all"):
        """versendet Newsletter"""
        logger.info("sent_newsletter in action")
        delete_testmail = False

        # hier wird der renderer bestimmt
        # zukünftig gibt es vielleicht mahr als einen
        # der view braucht eine Url, hier wird der url name verwendet
        # print('pk',pk)
        if pk == None:
            url = settings.DEFAULT_DOMAIN + reverse(view_name)
        else:
            url = settings.DEFAULT_DOMAIN + reverse(view_name, args=(pk,))
        if email == "@all":
            abonenten = NewsletterAbonnent.objects.filter(opt_in=True)
            logger.info("sent_newsletter: Email @all")
            # versende nicht ausversehen an alle
            # print("ausversehen an allen ;-)", email)
        else:
            logger.info("Testmail an %s", email)
            # Falls Testmail keine ABonentenadresse.. zum testen anlegen, zum Schluss löschen
            if not NewsletterAbonnent.objects.filter(email=email).exists():
                NewsletterAbonnent.objects.create(email=email, opt_in=True)
                delete_testmail = NewsletterAbonnent.objects.filter(email=email)
            abonenten = NewsletterAbonnent.objects.filter(email=email)  # lade Testuser

        # abonenten = NewsletterAbonnent.objects.filter(email = "christian.engler@35kino.de")

        self.anzahl = int(abonenten.count())
        subject = subject
        # from_email = settings.EMAIL_HOST_USER
        from_email = DEFAULT_FROM_EMAIL
        text_maker = html2text.HTML2Text()
        text_maker.ignore_images = True
        text_maker.ignore_tables = True
        html_body = requests.get(url).text
        text_body = text_maker.handle(html_body)

        connection = mail.get_connection()
        # Manually open the connection for bulk massages
        connection.open()
        for idx, abonent in enumerate(abonenten):
            # Für bulk tests
            # abonent.email = "christian.engler@35kino.de"
            # UNSUBSCRIBE
            # <a http://127.0.0.1:8000/newsletter/abmelden/' + abonent.email + '/' + abonent.salz>
            # abonent.email/abonent.salz für #changeme# in newsletter_render_today.html
            change = abonent.email + "/" + abonent.salz
            html_text = html_body.replace("#changeme#", change)
            text_text = text_body.replace("#changeme#", change)
            # message
            message = EmailMultiAlternatives(
                subject=subject,
                body=text_text,
                from_email=from_email,
                to=[abonent.email],
            )
            message.attach_alternative(html_text, "text/html")
            # message.send() # ohne bulk
            try:
                connection.send_messages(
                    [
                        message,
                    ]
                )  # bulke eine nach der anderen,
                print(idx, "gesendet an:", abonent.pk)
                logger.debug("NewsletterSent: %s gesendet an %s", idx, abonent.pk)
            except:
                print(
                    "### Fehler beim emailversand. Lösche ",
                    abonent.pk,
                    "mit mail",
                    abonent.email,
                )
                logger.warning("NewsletterSent: Fehler beim emailversand. Lösche")
                abonent.delete()
        connection.close()

        # versende controlmail
        self.beendet = datetime.datetime.now()
        timediff = self.beendet - self.gestartet
        text_body = (
            "start: "
            + str(self.gestartet)
            + " ende: "
            + str(self.beendet)
            + " benötigte Zeit: "
            + str(timediff)
            + " Anzahl: "
            + str(self.anzahl)
            + "\n"
            + text_body
        )
        message = EmailMultiAlternatives(
            subject=subject,
            body=text_body,
            from_email=from_email,
            to=["newsletter@kino35.de"],
        )
        message.send()
        self.save()
        # lösche TEstmail, fals zuvor nicht in DB
        if delete_testmail:
            delete_testmail.delete()
        # zeit auf Website
        return timediff


class Sondernewsletter(models.Model):
    titel = models.CharField(max_length=34, default="noch kein Titel!")
    text = models.TextField(default="hier sollte der Text stehen")
    erstellt = models.DateTimeField(auto_now_add=True)
    gesendet = models.DateTimeField(null=True, default=None)
    sende = models.DateTimeField(null=True, default=None)
    sender = models.ForeignKey(
        User, on_delete=models.SET_DEFAULT, null=True, default=None
    )  #
    bild_orig = models.ImageField(upload_to="filme/newsletter/", blank=True, null=True)
    bild = ImageSpecField(
        source="bild_orig",
        processors=[ResizeToFill(600, 300)],
        format="JPEG",
        options={"quality": 80},
    )
    bild_thumb = ImageSpecField(
        source="bild_orig",
        processors=[ResizeToFill(160, 80)],
        format="JPEG",
        options={"quality": 80},
    )

    def __str__(self):
        name = self.pk + "-" + self.titel
        return self.name
