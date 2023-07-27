from django import forms
#from django.contrib.admin import widgets  
from .models import Film, Event, NewsletterAbonnent,Comment, Sondernewsletter
from crispy_forms.helper import FormHelper
from django.forms import ClearableFileInput
import datetime


class FilmNeuForm(forms.ModelForm):
    class Meta:
         model = Film
         fields = ('name', 'interner_kommentar')

class InterneBewertung(forms.NumberInput):
    input_type = 'number'

class MyClearableFileInput(ClearableFileInput):
    template_name = 'widgets/customclearablefileinput.html'

class FilmBewertungForm(forms.ModelForm):
    class Meta:
        model = Film
        fields = ('name', 'trailer', 'website', 'plakat', 'interner_kommentar',
         'interne_bewertung_zahl', 'interne_bewerter_zahl', 'status','genre' )
        widgets = {
            'interne_bewertung_zahl': InterneBewertung(),
            'interne_bewerter_zahl': InterneBewertung(),

            'plakat': MyClearableFileInput(),
        }
        labels = {
            'trailer': ( ),
            'website': ( ),
            'plakat': ( ),
            'interne_bewertung_zahl': ('interne Bewertung'),
            'interne_bewerter_zahl': (),
            'status': ('Status')
        }
        help_texts = {
            'interne_bewertung_zahl': ('Wie viele sind für diesen Film'),
            'interne_bewerter_zahl': ('Wie viele haben abgestimmt'),

            'status': ('Wo findet sich der Film wieder? Sichtung, Vorauswahl, Planung oder im Archiv'),
        }

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['interne_bewertung_zahl'].widget.attrs.update({'min' : -2, 'max': 2})



class FilmForm(forms.ModelForm):
    class Meta:
        model = Film
        fields = ('name', 'trailer', 'website','plakat', 'director', 'countryOfOrigin', 'datePublished',
          'duration', 'genre','actors', 'fsk', 'description', 'hinweis', 'interner_kommentar',
           'status', 'film_komplett' )
        labels = {
            'director': ('Regie'),
            'duration': ("Spielzeit"),
            'actors': ('Schausspieler'),
            'datePublished': ('Jahr'),
            'countryOfOrigin': ('Land')
        }
        widgets = {
            'plakat': MyClearableFileInput(),
        }

class DateInput(forms.DateInput):
    input_type = 'date'

class TimeInput(forms.DateInput):
    input_type = 'time'
  
class SpielplanForm(forms.ModelForm):
    
    class Meta:
        model = Event
        fields = ( 'kategorie','film', 'ersatzfilm', 'termin', 'zeit' )
        labels = {
            'film': ( ),
            'ersatzfilm': ( ),
            'kategorie': ( ),
            'termin':(),
            'zeit':(),
        }
        widgets = {
            'termin': DateInput(format='%Y-%m-%d'),
            'zeit': TimeInput(format='%H:%M')
        }
# nutze .distinct() bei limit_choices_to
# https://stackoverflow.com/questions/51948640/using-limit-choices-to-on-a-fk-causes-multipleobjectsreturned-error-on-model
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['film'].queryset = self.fields['film'].queryset.distinct()
        self.fields['ersatzfilm'].queryset = self.fields['ersatzfilm'].queryset.distinct()

       
class EventDiensteForm(forms.ModelForm):
    next = forms.CharField(required=False)

    class Meta:
        model = Event
        fields = ('theke1', 'theke2', 'kasse', 'vorfuehrer', 'text_intern',)
   
class EventDetailForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ('event_film_confirmed', 'text_intern', 'text_extern','theke1', 'theke2', 'kasse', 'vorfuehrer',  )
        labels = {
            'event_film_confirmed': ('Film zum Termin bestätigt' ),

        }
        # help_texts = {
        #     'kategorie': ('Dies sorgt für die richtige Anzeige auf der Website.'),
        #     'termin': ('Den Tag der Vorführung angeben.'),
        # }
        # error_messages = {        }

class EventNeuForm(forms.ModelForm):
    wdh = forms.IntegerField(initial = 1, label = "Wiederholungen", min_value= 1, max_value= 20,
      help_text = 'Wöchentliche Wiederholungen dieser Veranstaltungsreihe anlegen.' )
    zeit = forms.TimeField(widget=TimeInput(), initial = '20:30', label = "Beginn")
    class Meta:
        model = Event
        fields = ('termin', 'kategorie',)
        widgets = {
            'termin': DateInput()
        }
        labels = {
            'kategorie': ('Kategorie auswählen'),
        }

class NewsletterForm(forms.ModelForm):
    class Meta:
        model = Sondernewsletter
        fields = ('titel', 'text', 'bild_orig',)
        widgets = {
            'bild_orig': MyClearableFileInput(),
            # 'sende': DateInput()
        }
        labels = {
            'bild_orig': ('Bild - kann aber muss nicht (Bild wird in 600x300 dargestellt)'),
        }
        
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('author', 'kommentar',)

class EventForm(forms.ModelForm):
    class Meta:
       model = Event
       fields = ( 'termin','text_intern',)

class NewsletterAboForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(NewsletterAboForm, self).__init__(*args, **kwargs)
        self.fields['email'].initial = '@'
    
    class Meta:
       model = NewsletterAbonnent
       fields = ( 'email',)
       labels = {
            'email': (),
        }


