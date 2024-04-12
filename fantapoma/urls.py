from django.urls import path, include

from . import views
from fantapoma.views import *

app_name = 'fantapoma'

urlpatterns = [
        path('', views.index, name='index'),
        path('mycrew/', MyCrewView.as_view(), name='mycrew'),
        path('marketplace/', FantaAthleteView.as_view(), name='marketplace'),
        path('view_athlete/<int:id>', views.view_athlete, name='view-athlete'),
        path('leaderboard', LeaderboardView.as_view(), name='leaderboard'),
        path('statistics/', StatisticsView.as_view(), name='statistics'),
        path('view_crew/<str:pk>/', ViewCrew.as_view(), name='view-crew'),
        path('view_crew/', ViewCrew.as_view(), name='view-crew'),
        # Specials
        path('special-market', ListSpecialsView.as_view(), name='special-market'),
        path('buy-special/<int:special_id>/', BuySpecialView.as_view(), name='buy_special'),
        path('sell-special/<int:special_id>/', SellSpecialView.as_view(), name='sell_special'),
        # Aftermatch Points
        path('submit-points/<int:athlete_id>/', UpdatePointsView.as_view(), name='submit-points'),
        path('submit-points/', UpdatePointsView.as_view(), name='submit-points'),
        path('athletes/', RawFantaAthleteListView.as_view(), name='athlete-list'),
        # Utilities
        path('give-points/', GivePointsView.as_view(), name='give-points'),
        path('create-special/', CreateSpecialView.as_view(), name='create-special'),
    ]
