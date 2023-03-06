from django.urls import path

from . import views
from fantapoma.views import MyCrewView, AthleteView, LeaderboardView, ViewCrew, CreateSpecialView, ListSpecialsView, UpdatePointsView

urlpatterns = [
        path('', views.index, name='fantapoma'),
        path('mycrew/', MyCrewView.as_view(), name='mycrew'),
        path('marketplace/', AthleteView.as_view(), name='marketplace'),
        path('view_athlete/<int:id>', views.view_athlete, name='view-athlete'),
        path('leaderboard', LeaderboardView.as_view(), name='leaderboard'),
        path('view_crew/<str:pk>/', ViewCrew.as_view(), name='view-crew'),
        path('view_crew/', ViewCrew.as_view(), name='view-crew'),
        path('create_special', CreateSpecialView.as_view(), name='create-special'),
        path('view_specials', ListSpecialsView.as_view(), name='view-specials'),
        path('submit-points/', UpdatePointsView.as_view(), name='submit-points'),
    ]
