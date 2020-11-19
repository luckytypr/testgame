from django.shortcuts import render

from .forms import TournamentCreateForm
from .models import Tournament, TournamentParticipant


def tournament_list(request, *args, **kwargs):
    tournaments = Tournament.objects.all()
    new_tournament = None
    if request.method == "POST":
        form = kwargs.get('form', None)
        if form is not None:
            new_tournament = form.instance

    deleted_tournament = kwargs.get('deleted_tournament', None)

    for tournament in tournaments:
        tournament.fields = dict(
            (
                field.name,
                field.value_to_string(tournament)
            ) for field in tournament._meta.fields
        )

    return render(request, 'tournaments/tournaments_list.html', {
        'new_tournament': new_tournament,
        'deleted_tournament': deleted_tournament,
        'tournaments': tournaments,
    })


def tournament_create(request, *args, **kwargs):

    if request.method == "POST":
        form = TournamentCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return tournament_list(request, form=form)

    form = TournamentCreateForm()

    return render(request, 'tournaments/tournaments_create.html',
                  {'form': form})


def tournament_delete(request, id):
    try:
        instance = Tournament.objects.get(id=id)
        instance.delete()
    except Tournament.DoesNotExist as e:
        return render(request, 'core/404.html')

    return tournament_list(request, deleted_tournament=instance)


def tournament_retrieve(request, id, **kwargs):

    new_participant = None
    if request.method == "POST":
        new_participant = kwargs.get('new_participant', None)

    deleted_participant = kwargs.get('deleted_participant', None)

    try:
        instance = Tournament.objects.get(id=id)
    except Tournament.DoesNotExist as e:
        return render(request, 'core/404.html')

    participants = instance.participants.all()
    participants = sorted(participants, key=lambda m: m.points, reverse=True)

    return render(request, 'tournaments/tournaments_retrieve.html', {
        'tournament': instance,
        'participants': participants,
        'participants_count': len(participants),
        'new_participant': new_participant,
        'deleted_participant': deleted_participant,
    })


def tournament_participant_delete(request, id, participant_id):

    try:
        instance = TournamentParticipant.objects.get(id=participant_id)
        instance = instance.delete()
    except Tournament.DoesNotExist as e:
        return render(request, 'core/404.html')

    return tournament_retrieve(request, id, deleted_participant=instance)