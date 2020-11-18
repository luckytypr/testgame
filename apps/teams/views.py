from .forms import TeamCreateForm
from apps.tournaments.views import tournament_retrieve
from apps.tournaments.models import Tournament, TournamentParticipant
from django.shortcuts import render
from pprint import pprint
from .models import Team
from apps.core.utils import get_required_participant_number, get_not_attended_team


def teams_create(request, tournament_id):

    try:
        tournament = Tournament.objects.get(id=tournament_id)
    except Tournament.DoesNotExist:
        return render(request, 'core/404.html')

    if request.method == "POST":
        form = TeamCreateForm(request.POST)
        if form.is_valid():
            team_name = form.cleaned_data.get('name', None)
            if team_name is None or team_name == "":
                new_team = get_not_attended_team(tournament)
            else:
                form.save()
                new_team = form.instance

            new_participant = TournamentParticipant.objects.create(
                tournament=tournament, team=new_team
            )

            return tournament_retrieve(
                request,
                tournament_id,
                new_participant=new_participant,
            )

    form = TeamCreateForm()

    return render(request, 'teams/teams_create.html',
                  {'form': form})


def teams_create_randomly(request, tournament_id):


    try:
        tournament = Tournament.objects.get(id=tournament_id)
    except Tournament.DoesNotExist:
        return render(request, 'core/404.html')

    participant_num = tournament.participants.count()
    required_participant_num = get_required_participant_number(participant_num)

    participant_pool = []
    for _ in range(required_participant_num):
        not_attended_team = get_not_attended_team(tournament)
        participant_instance = TournamentParticipant(
            tournament=tournament,
            team=not_attended_team,
        )
        participant_pool.append(participant_instance)
    TournamentParticipant.objects.bulk_create(participant_pool)

    return tournament_retrieve(
        request,
        tournament_id,
    )


def teams_retrieve(request, id, tournament_id):

    try:
        team_instance = Team.objects.get(id=id, participantions__tournament_id=tournament_id)
    except Team.DoesNotExist as e:
        return render(request, 'core/404.html')

    return render(request, 'teams/teams_retrieve.html', {'team': team_instance})

# def tournament_team(request, tournament_id)
