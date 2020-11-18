from apps.teams.models import Team
from apps.games.models import Game
from apps.tournaments.models import TournamentParticipant
from apps.core import TournamentStages


def get_required_participant_number(current_participant_number: int):
    TOURNAMENT_PARTICIPANT_NUM = 16
    required_participant_num = TOURNAMENT_PARTICIPANT_NUM - current_participant_number
    return max(0, required_participant_num)


def get_not_attended_team(tournament):
    enrolled_team_ids = tournament.participants.values_list('team_id', flat=True)
    while True:
        team_name = Team.generate_name()
        team_is_enrolled = Team.objects.filter(
            name=team_name, id__in=enrolled_team_ids
        ).exists()

        if team_is_enrolled:
            continue

        team, created = Team.objects.get_or_create(name=team_name)
        return team


def play_group_games(tournament, participants):

    if not isinstance(participants, list):
        participants = list(participants.all())

    for index, right_participant in enumerate(participants):
        for left_participant in participants[index::]:
            if right_participant != left_participant:
                game, _ = Game.objects.get_or_create(
                    tournament=tournament,
                    left_player=left_participant,
                    right_player=right_participant,
                    stage=TournamentStages.GROUP_STAGE
                )
                game.play_game()


def get_division_result_matrix(division_queryset):
    if not isinstance(division_queryset, list):
        division_queryset = list(division_queryset.all())

    result_matrix = []
    for i, participant in enumerate(division_queryset):
        result_matrix.append({
            'participant_name': participant.team.name,
            'participant_in_game': participant.in_game,
            'games': []
        })
        for opponent_participant in division_queryset:
            if participant == opponent_participant:
                cell_data = {
                    'self': True,
                }
            else:
                game = Game.objects.get_game(participant, opponent_participant)

                if game is None:
                    cell_data = {
                        'self': False,
                    }
                else:
                    cell_data = {
                        'self': False,
                        'left_score': game.left_player_score,
                        'right_score': game.right_player_score,
                        'winner': game.winner
                    }
            result_matrix[i]['games'].append(cell_data)

    return result_matrix


def mark_eliminated_from_division(division_qs):
    PRESERVED_PARTICIPANT_NUMBER = 4

    division_qs = sorted(division_qs, key=lambda m: m.points, reverse=True)

    eliminated_participants = division_qs[PRESERVED_PARTICIPANT_NUMBER::]

    participant_update_pool = []
    for participant in eliminated_participants:
        participant.in_game = False
        participant_update_pool.append(participant)

    TournamentParticipant.objects.bulk_update(participant_update_pool, ('in_game',),)


def get_stage_name(participant_number):
    if participant_number == 16:
        return TournamentStages.GROUP_STAGE
    elif participant_number == 8:
        return TournamentStages.QUARTER_FINAL
    elif participant_number == 4:
        return TournamentStages.SEMI_FINAL
    elif participant_number == 2:
        return TournamentStages.FINAL
    return TournamentStages.PREPARATION