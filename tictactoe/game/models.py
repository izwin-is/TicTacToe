from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import json

# class User(models.Model):
#     nick = models.CharField(max_length=30)
#     rating = models.IntegerField(default=500)
#     time_register = models.DateTimeField(auto_now_add=True)
#     time_last_game = models.DateTimeField()
#     # def get_absolute_url:
#     #     pass Тут нужно прописать, как игрок будет отображаться на сайте
#     class Meta:
#         verbose_name = 'Игрок'
#         verbose_name_plural = 'Игроки'

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=500)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

class Games(models.Model):
    player_1 = models.ForeignKey(User, on_delete=models.PROTECT, related_name='player_1')
    player_2 = models.ForeignKey(User, on_delete=models.PROTECT, related_name='player_2')
    winner = models.ForeignKey(User, on_delete=models.PROTECT, related_name='winner', null=True)
    first = models.ForeignKey(User, on_delete=models.PROTECT, related_name='first')
    field = models.CharField(default=json.dumps([[0, 0, 0], [0, 0, 0], [0, 0, 0]]), max_length=9)
    href_name = models.IntegerField(blank=True)
    game_time = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name = 'Игра'
        verbose_name_plural = 'Игры'

class WaitingGame(models.Model):
    waiting_player = models.ForeignKey(User, on_delete=models.PROTECT, related_name='waiting_player')
    class Meta:
        verbose_name = 'Игра в ожидании'
        verbose_name_plural = 'Игры в ожидании'

    @property
    def username(self):
        return User.objects.get(pk=self.waiting_player.pk).username

