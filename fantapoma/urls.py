from django.urls import path

from . import views
from fantapoma.views import MyCrewView, FantaAthleteView, LeaderboardView, ViewCrew, CreateSpecialView, ListSpecialsView, UpdatePointsView, RawFantaAthleteListView, EventsView, StatisticsView

urlpatterns = [
        path('', views.index, name='fantapoma'),
        path('mycrew/', MyCrewView.as_view(), name='mycrew'),
        path('marketplace/', FantaAthleteView.as_view(), name='marketplace'),
        path('view_athlete/<int:id>', views.view_athlete, name='view-athlete'),
        path('leaderboard', LeaderboardView.as_view(), name='leaderboard'),
        path('events', EventsView.as_view(), name='events'),
        path('statistics/', StatisticsView.as_view(), name='statistics'),
        path('view_crew/<str:pk>/', ViewCrew.as_view(), name='view-crew'),
        path('view_crew/', ViewCrew.as_view(), name='view-crew'),
        path('create_special', CreateSpecialView.as_view(), name='create-special'),
        path('view_specials', ListSpecialsView.as_view(), name='view-specials'),
        path('submit-points/<int:athlete_id>/', UpdatePointsView.as_view(), name='submit-points'),
        path('submit-points/', UpdatePointsView.as_view(), name='submit-points'),
        path('athletes/', RawFantaAthleteListView.as_view(), name='athlete-list'),
    ]
