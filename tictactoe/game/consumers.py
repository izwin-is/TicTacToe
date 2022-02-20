import json
from channels.generic.websocket import WebsocketConsumer
from django.contrib.auth.models import User
from channels.db import database_sync_to_async
from asgiref.sync import async_to_sync
from game.models import *
from random import randint


class ViewConsumer(WebsocketConsumer):
    def connect(self):
        self.room_group_name = 'test'
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

    def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        if data['type'] == 'creation':
            game_id = async_to_sync(self.create_waiting_game)(int(data['id']))
            if game_id:
                async_to_sync(self.channel_layer.group_send)(
                    self.room_group_name,
                    {
                        'type': 'creation',
                        'player_id': data['id'],
                        'game_id': game_id
                    }
                )
        elif data['type'] == 'removal':
            game_id = async_to_sync(self.remove_waiting_game)(int(data['id']))
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'removal',
                    'player_id': data['id'],
                    'game_id': game_id
                }
            )
        elif data['type'] == 'join':
            id_2 = async_to_sync(self.get_player_id)(int(data['game_id']))
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'join',
                    'id_1': data['player_id'],
                    'id_2': id_2,
                    'game_id': data['game_id']
                }
            )

    @database_sync_to_async
    def create_waiting_game(self, id):
        if WaitingGame.objects.filter(waiting_player=User.objects.get(pk=id)):
            return None

        w = WaitingGame(waiting_player=User.objects.get(pk=id))
        w.save()
        return w.pk

    @database_sync_to_async
    def remove_waiting_game(self, id):
        w = WaitingGame.objects.get(waiting_player=User.objects.get(pk=id))
        ans = w.pk
        w.delete()
        return ans

    @database_sync_to_async
    def get_player_id(self, id):
        w = WaitingGame.objects.get(pk=id)
        ans = w.waiting_player.id
        w.delete()
        return ans


    def join(self, event):
        # print(event)
        self.send(text_data=json.dumps({
            'type': 'join',
            'id_1': event['id_1'],
            'id_2': str(event['id_2']),
            'game_id': event['game_id']
        }))

    def creation(self, event):
        # print('+++++++++++', event['game_id'])
        self.send(text_data=json.dumps({
            'type': 'creation',
            'player_id': event['player_id'],
            'game_id': event['game_id']
        }))

    def removal(self, event):
        self.send(text_data=json.dumps({
            'type': 'removal',
            'player_id': event['player_id'],
            'game_id': event['game_id']
        }))
# class ChatConsumer(WebsocketConsumer):
#     def connect(self):
#         self.room_name = self.scope['url_route']['kwargs']['room_name']
#         self.room_group_name = f'chat_{self.room_name}'
#
#         async_to_sync(self.channel_layer.group_add)(
#             self.room_group_name,
#             self.channel_name
#         )
#         self.accept()
#
#
#     def receive(self, text_data=None, bytes_data=None):
#         text_data_json = json.loads(text_data)
#         message = text_data_json['message']
#         username = text_data_json['username']
#
#         # print(value)
#         async_to_sync(self.channel_layer.group_send)(
#             self.room_group_name,
#             {
#                 'type': 'message',
#                 'message': message,
#                 'username': username
#             }
#         )
#     #
#     def message(self, event):
#         message = event['message']
#         username = event['username']
#         self.send(text_data=json.dumps({
#             'type': 'message',
#             'message': message,
#             'username': username
#         }))
