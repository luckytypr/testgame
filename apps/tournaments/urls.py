from django.urls import path, include
from . import views
from . import stage_views

app_name = 'tournaments'

urlpatterns = [
    path('create/', views.tournament_create, name='create'),
    path('<int:id>/', views.tournament_retrieve, name='retrieve'),
    path('<int:id>/delete/', views.tournament_delete, name='delete'),
    path('<int:id>/participants/<int:participant_id>',
         views.tournament_participant_delete,
         name='delete-participant'),

    path('<int:id>/group_stage/start/', stage_views.tournament_group_stage_start, name='group-stage-start'),
    path('<int:id>/group_stage/results/', stage_views.tournament_group_stage_result, name='group-stage-result'),

    path('<int:id>/stage/start/', stage_views.tournament_playoff_start, name='playoff-start'),
    path('<int:id>/stage/results/', stage_views.tournament_playoff_result, name='playoff-result'),

    path('', views.tournament_list, name='list'),
]