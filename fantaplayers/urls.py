from django.urls import include, path

from fantaplayers.views import ProfileView, UpdateProfile, CreatePlayer

app_name = 'fantaplayers'

urlpatterns = [
        path('', include('django.contrib.auth.urls')),
        path('register', CreatePlayer.as_view(), name='register'),
        path('profile/<str:pk>', ProfileView.as_view(), name='profile'),
        path('update_profile/<str:pk>', UpdateProfile.as_view(), name='update-profile'),
    ]

