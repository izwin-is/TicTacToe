from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

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
    winner = models.ForeignKey(User, on_delete=models.PROTECT, related_name='winner')
    game_time = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name = 'Игра'
        verbose_name_plural = 'Игры'

