from django.contrib import admin

from .models import *

admin.site.register(Profile)
admin.site.register(Games)
admin.site.register(WaitingGame)