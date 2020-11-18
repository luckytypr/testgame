from apps.tournaments.models import Tournament
from django.shortcuts import render
from apps.games.models import Game
from apps.teams.models import Team


def tournament_view(function):
    def wrapper(request, **kwargs):
        tournament_id = kwargs.get('tournament_id', kwargs.get('id'))
        try:
            tournament = Tournament.objects.get(id=tournament_id)
        except Tournament.DoesNotExist:
            return render(request, 'core/404.html')
        return function(request, tournament)

    return wrapper


def team_view(function):
    def wrapper(request, **kwargs):
        team_id = kwargs.get('team_id', kwargs.get('id'))
        try:
            team = Team.objects.get(id=team_id)
        except Tournament.DoesNotExist:
            return render(request, 'core/404.html')
        return function(request, team)

    return wrapper


def game_view(function):
    def wrapper(request, **kwargs):
        game_id = kwargs.get('game_id', kwargs.get('id'))
        try:
            game = Game.objects.get(id=game_id)
        except Tournament.DoesNotExist:
            return render(request, 'core/404.html')
        return function(request, game)

    return wrapper

