from django.shortcuts import render
from .models import Tournament, TournamentParticipant
from . import Divisions
from ..games.models import Game
from ..games import WinnerStatus
from ..core import TournamentStages
from ..core.decorators import tournament_view
from apps.core.utils import (
    play_group_games,
    get_division_result_matrix,
    mark_eliminated_from_division,
    get_stage_name
)


@tournament_view
def tournament_group_stage_start(request, tournament):
    tournament.change_stage(TournamentStages.GROUP_STAGE)

    Tournament.objects.order_by()
    first_division = tournament.participants.exclude(
        division=Divisions.SECOND_DIVISION
    )

    PARTICIPANT_NUMBER_PER_DIVISION = 8
    if first_division.count() > PARTICIPANT_NUMBER_PER_DIVISION:
        tournament.participants.update(division=Divisions.NOT_ASSIGNED)
        first_division = first_division.order_by('?')[:PARTICIPANT_NUMBER_PER_DIVISION]
        for participant in first_division:
            participant.division = Divisions.FIRST_DIVISION
            participant.save()

    second_division = tournament.participants.exclude(division=Divisions.FIRST_DIVISION)
    second_division.update(division=Divisions.SECOND_DIVISION)

    return render(request, 'tournaments/tournaments_group_stage.html',
                  {
                      'tournament': tournament,
                      'first_division_participants': first_division,
                      'second_division_participants': second_division,
                  })


@tournament_view
def tournament_group_stage_result(request, tournament):

    first_division = tournament.participants.filter(
        division=Divisions.FIRST_DIVISION
    ).order_by('team__name').all()
    second_division = tournament.participants.filter(
        division=Divisions.SECOND_DIVISION
    ).order_by('team__name').all()

    play_group_games(tournament, first_division)
    play_group_games(tournament, second_division)

    mark_eliminated_from_division(first_division)
    mark_eliminated_from_division(second_division)

    first_division_result_matrix = get_division_result_matrix(first_division)
    second_division_result_matrix = get_division_result_matrix(second_division)

    return render(request, 'tournaments/tournaments_group_stage_results.html',
                  {
                      'tournament': tournament,
                      'first_division_participants': first_division,
                      'first_division_matrix': first_division_result_matrix,
                      'second_division_participants': second_division,
                      'second_division_matrix': second_division_result_matrix,
                  })


@tournament_view
def tournament_playoff_start(request, tournament):
    preserved_participants_qs = tournament.participants.filter(in_game=True)

    preserved_participants = sorted(
        preserved_participants_qs,
        key=lambda participant: participant.points,
        reverse=True
    )

    participants_number = len(preserved_participants)
    if participants_number == 1:
        participant = preserved_participants_qs.first()
        tournament.is_active = False
        tournament.save()

        return render(request, 'tournaments/tournaments_winner.html',
                      {
                          'tournament': tournament,
                          'participant': participant,
                      })

    elif participants_number % 2 == 0:
        stage_name = get_stage_name(participants_number)
        tournament.change_stage(stage_name)
        games_pool = []
        for i in range(participants_number//2):
            """      
                Since preserved_participants
                list is sorted, right players will be 
                the participants with highest score
            """
            right_participant = preserved_participants[i]
            left_participant = preserved_participants[participants_number - i - 1]
            game, _ = Game.objects.get_or_create(
                tournament=tournament,
                left_player=left_participant,
                right_player=right_participant,
                stage=stage_name,
            )
            games_pool.append(game)

        games_pool = sorted(
            games_pool,
            key=lambda m: m.right_player.team.name,
            reverse=True
        )
        return render(request, 'tournaments/tournaments_playoff_stage.html',
                      {
                          'tournament': tournament,
                          'games': games_pool,
                      })
    else:
        print("It is impossible to have odd number of teams ")
        return render(request, 'core/404.html')


@tournament_view
def tournament_playoff_result(request, tournament):
    current_stage = tournament.current_stage

    current_games = tournament.games.filter(stage=current_stage).order_by('-right_player__team__name')

    for game in current_games:
        game.play_game()
        if game.winner == WinnerStatus.LEFT:
            eliminated_participant = game.right_player
        else:
            eliminated_participant = game.left_player
        eliminated_participant.in_game = False
        eliminated_participant.save()

    return render(request, 'tournaments/tournaments_playoff_stage_results.html',
                  {
                      'tournament': tournament,
                      'games': current_games,
                  })