from django.test import TestCase

from .models import Film


class FilmModelTests(TestCase):

    def programmauswahl_ein(self):
        """
        Übung: setze flag.
        """
        film = Film(name = "testfilm")
        self.assertIs( Film.programmauswahl_ein(film), False)

