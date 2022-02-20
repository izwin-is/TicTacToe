from django.urls import re_path, path
from . import consumers

websocket_urlpatterns = [
    # re_path(r'ws/room/(?P<room_name>\w+)/$', consumers.ChatConsumer.as_asgi()),
    path('ws/', consumers.ViewConsumer.as_asgi())
]