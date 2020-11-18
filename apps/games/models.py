from django.db import models
from . import WinnerStatus
from ..core import TournamentStages
from ..core.models import TimeStampModel
from random import randint


class GameManager(models.Manager):

    def get_game(self, participant_one, participant_two):
        try:
            game = self.get(left_player=participant_one, right_player=participant_two)
            return game
        except:
            pass

        try:
            game = self.get(right_player=participant_one, left_player=participant_two)
            return game
        except:
            pass

        return None



class Game(TimeStampModel):

    tournament = models.ForeignKey(
        'tournaments.Tournament',
        related_name='games',
        on_delete=models.CASCADE
    )

    left_player = models.ForeignKey(
        'tournaments.TournamentParticipant',
        related_name='as_left_player',
        on_delete=models.SET_NULL,
        null=True
    )

    right_player = models.ForeignKey(
        'tournaments.TournamentParticipant',
        related_name='as_right_player',
        on_delete=models.SET_NULL,
        null=True
    )

    stage = models.CharField(
        max_length=20,
        choices=TournamentStages.choices,
        default=TournamentStages.PREPARATION,
        db_index=True, )

    left_player_score = models.IntegerField(default=0, blank=True)
    right_player_score = models.IntegerField(default=0, blank=True)

    winner = models.CharField(
        max_length=20,
        choices=WinnerStatus.choices,
        default=WinnerStatus.UNDERFINED,
        db_index=True,
    )

    objects = GameManager()

    def play_game(self):
        if self.winner != WinnerStatus.UNDERFINED:
            """Game has already been played and you do not need to replay it"""
            return

        self.left_player_score = randint(0, 10)
        self.right_player_score = randint(0, 10)

        if self.left_player_score > self.right_player_score:
            self.winner = WinnerStatus.LEFT
        elif self.right_player_score > self.left_player_score:
            self.winner = WinnerStatus.RIGHT
        else:
            self.winner = WinnerStatus.DRAW

        self.save(update_fields=[
            'left_player_score', 'right_player_score', 'winner'
        ])

    class Meta:
        verbose_name = "Game"
        verbose_name_plural = "Games"
