from django.urls import path, include
from . import views

app_name = 'teams'

urlpatterns = [
    path('create/', views.teams_create, name='create'),
    path('auto-create/', views.teams_create_randomly, name='auto-create'),
    path('<int:id>/', views.teams_retrieve, name='retrieve'),

]