from .forms import TeamCreateForm
from apps.tournaments.views import tournament_retrieve
from apps.tournaments.models import Tournament, TournamentParticipant
from django.shortcuts import render

from apps.core.utils import get_required_participant_number, get_not_attended_team
from apps.core.decorators import tournament_view, team_view


@tournament_view
def teams_create(request, tournament):

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
                tournament.id,
                new_participant=new_participant,
            )
    else:
        form = TeamCreateForm()
        return render(request, 'teams/teams_create.html', {'form': form})


@tournament_view
def teams_create_randomly(request, tournament):
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
        tournament.id,
    )


@team_view
def teams_retrieve(request, team):
    return render(request, 'teams/teams_retrieve.html',
                  {'team': team})

