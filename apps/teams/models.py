from random import randint

from ..core import ADJECTIVES, NOUNS, CITIES
from ..core.models import RandomNameGeneratedModel, TimeStampModel


class Team(RandomNameGeneratedModel, TimeStampModel):

    @property
    def scores(self):
        return sum(participation.points for participation in self.participantions.all())

    @classmethod
    def generate_name(cls):
        adjective = ADJECTIVES[randint(0, len(ADJECTIVES)-1)]
        noun = NOUNS[randint(0, len(NOUNS)-1)]
        city = CITIES[randint(0, len(CITIES)-1)]
        return f"{adjective.upper()} {noun.upper()} of {city.upper()}"

    class Meta:
        verbose_name = "Team"
        verbose_name_plural = "Teams"