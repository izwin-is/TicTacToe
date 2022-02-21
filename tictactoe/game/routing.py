from django.urls import re_path, path
from . import consumers

websocket_urlpatterns = [
    path('ws/game/<int:game_id>/', consumers.PlayConsumer.as_asgi()),
    path('ws/', consumers.ViewConsumer.as_asgi())
]