from django.urls import path
from game.views import *

urlpatterns = [
    path('', HomePage.as_view(), name='home'),
    path('enter/', RegisterUser.as_view(), name='enter'),
    path('play/', PlayPage.as_view(), name='play'),
    path('profile/', profile, name='profile'),
    path('liders/', liders, name='liders'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('game/<int:game_id>/', GameView.as_view(), name='game')
]