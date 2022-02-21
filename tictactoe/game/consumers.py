import json
from channels.generic.websocket import WebsocketConsumer
from django.contrib.auth.models import User
from channels.db import database_sync_to_async
from asgiref.sync import async_to_sync
from game.models import *
from random import choice



class PlayConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['game_id']
        self.room_group_name = f'room_{self.room_name}'
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        field = async_to_sync(self.get_field)()
        # async_to_sync(self.channel_layer.group_send)(
        #     self.room_group_name,
        #     {
        #         'type': 'connection',
        #         'field': field
        #     }
        # )
        self.accept()
        self.send(json.dumps({
            'type': 'connection',
            'field': field
        }))

    # def connection(self, event):
    #     self.send(json.dumps(event))

    @database_sync_to_async
    def get_field(self):
        return Games.objects.get(href_name=int(self.room_name)).field

    def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        if data['type'] =='move':
            result = async_to_sync(self.make_move)(data)
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'move',
                    'id': data['id'],
                    'position': data['position'],
                    'result': result
                }
            )
    def move(self, event):
        self.send(json.dumps(event))



    @database_sync_to_async
    def make_move(self, data):
        field = Games.objects.get(href_name=int(self.room_name))
        field_mas = json.loads(field.field)
        i = int(data['position'][0])
        j = int(data['position'][1])
        if field_mas[i][j] == 0:
            field_mas[i][j] = int(data['id'])
            field.field = json.dumps(field_mas)
            field.save(update_fields=['field'])
            return self.check(field_mas)
        else:
            return False

    def check(self, field_mas):
        for i in range(3):
            if field_mas[0][i] == field_mas[1][i] == field_mas[2][i] != 0:
                return 1
            if field_mas[i][0] == field_mas[i][1] == field_mas[i][2] != 0:
                return 1
        if field_mas[0][0] == field_mas[1][1] == field_mas[2][2] != 0:
            return 1
        if field_mas[0][2] == field_mas[1][1] == field_mas[2][0] != 0:
            return 1
        if field_mas[0][0] != 0 and field_mas[0][1] != 0 and field_mas[0][2] != 0 and \
        field_mas[1][0] != 0 and field_mas[1][1] != 0 and field_mas[1][2] != 0 and \
        field_mas[2][0] != 0 and field_mas[2][1] != 0 and field_mas[2][2] != 0:
            return 2




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
                        'game_id': game_id,
                        'username': data['username']
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
            id_2 = async_to_sync(self.get_player_id)(data)
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
    def get_player_id(self, data):
        w = WaitingGame.objects.get(pk=int(data['game_id']))
        ans = w.waiting_player.id
        w.delete()
        w = Games(player_1=User.objects.get(pk=int(data['player_id'])),
                  player_2=User.objects.get(pk=int(ans)),
                  href_name=int(data['game_id']),
                  first=choice([User.objects.get(pk=int(data['player_id'])), User.objects.get(pk=int(ans))]))
        w.save()
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
            'game_id': event['game_id'],
            'username': event['username']
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
