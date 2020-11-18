from django.db import models

from random import randint
from ..core.models import RandomNameGeneratedModel, TimeStampModel
from ..core import ADJECTIVES, NOUNS, TournamentStages
from . import Divisions


class Tournament(RandomNameGeneratedModel, TimeStampModel):

    is_active = models.BooleanField(default=True, blank=True)
    current_stage = models.CharField(
        max_length=20,
        choices=TournamentStages.choices,
        default=TournamentStages.PREPARATION,
        db_index=True,)

    def change_stage(self, new_stage):
        self.current_stage = new_stage
        self.save(update_fields=('current_stage',))

    def generate_name(self):
        adjective = ADJECTIVES[randint(0, len(ADJECTIVES)-1)]
        noun = NOUNS[randint(0, len(NOUNS)-1)]
        return f"{adjective.upper()} {noun.upper()} TOURNAMENT"

    class Meta:
        verbose_name = "Tournament"
        verbose_name_plural = "Tournament"


class TournamentParticipant(models.Model):

    @property
    def points(self):
        games_as_left_player = self.as_left_player.all()
        points = sum(game.left_player_score for game in games_as_left_player)

        games_as_right_player = self.as_right_player.all()
        points += sum(game.right_player_score for game in games_as_right_player)
        # TODO: Count points and staff
        return points

    tournament = models.ForeignKey(
        'tournaments.Tournament',
        related_name='participants',
        on_delete=models.CASCADE
    )

    team = models.ForeignKey(
        'teams.Team',
        related_name='participantions',
        on_delete=models.CASCADE
    )

    in_game = models.BooleanField(default=True)
    division = models.CharField(
        max_length=20,
        choices=Divisions.choices,
        default=Divisions.NOT_ASSIGNED,
    )


    class Meta:
        verbose_name = "Tournament participant"
        verbose_name_plural = "Tournament participants"
