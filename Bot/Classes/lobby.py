from ..Keyboards.keyboard import Keyboard, Button
from .Game.roles import *
from .Game.variables import *
from ..functions import find_user_by_username
import random


def get_new_id(lobbies):
    ids = []
    if len(lobbies) == 0:
        return 1

    for lobby in lobbies:
        ids.append(lobby.id)
    return max(ids) + 1


class Lobby:
    def __init__(self, lobbies, name, autor, bot, count=3):
        self.id = get_new_id(lobbies)
        self.name = name
        self.autor = autor
        if autor:
            self.users = [autor]
        else:
            self.users = []
        self.bot = bot
        self.count = count  # нужно юзеров для старта
        self.locked = False
        self.time = DAY

    def add_user(self, user):
        if len(self.users) == self.count:
            return False

        self.users.append(user)
        user.lobby = self

        for user in self.users:
            self.lobby_menu(user)

        if len(self.users) == self.count:
            self.start_game()

    def remove_user(self, del_user):
        self.users.remove(del_user)
        del_user.lobby = None

        if len(self.users) == 0:
            self.bot.lobbies.remove(self)
        else:
            for user in self.users:
                if user is not del_user:
                    self.bot.send_message(user.chat_id, f'{del_user.username} покинул лобби')
                    self.lobby_menu(user)

    def get_menu_string(self, user):
        text = f'---= Вы в лобби {self.name} =---\n' \
               f'Сейчас игроков: {len(self.users)}/{self.count}\n\n' \
               f'Игроки: \n'
        for user in self.users:
            text += f"{user}\n"
        return text

    def lobby_menu(self, user):
        text = self.get_menu_string(user)
        keyboard = Keyboard([[Button('выйти')]])
        self.bot.send_message(user.chat_id, text, keyboard)
        user.next_message_handler = self.lobby_menu_handler

    def lobby_menu_handler(self, user, text):
        if text == 'выйти':
            self.remove_user(user)
            self.bot.router.main_menu(user)

    def __str__(self):
        return f'{self.id} <{self.name}> ({len(self.users)} / {self.count})'

    def start_game(self):
        self.locked = True
        self.game_preparing()
        for user in self.users:
            self.bot.send_message(user.chat_id, 'Игра началась!')
            self.send_role_info(user)
            self.in_game_menu(user)

    def game_preparing(self):
        for user in self.users:
            user.role = CIVILIAN
            user.votes_number = 0

        user = random.choice(self.users)
        user.role = MAFIA

    def send_role_info(self, user):
        if user.role == MAFIA:
            self.bot.send_message(user.chat_id, 'Ты мафия. Радуйся. Кикни всех.')
        elif user.role == CIVILIAN:
            self.bot.send_message(user.chat_id, 'Ты мирный житель. Не ной.')

    def in_game_menu(self, user):
        if self.time == DAY:
            self.day_menu(user)
        else:
            self.night_menu(user)

    def day_menu(self, user):
        self.bot.send_message(user.chat_id, 'Сейчас происходит обсуждение. Пиши прям сюда.\n'
                                            'Для голоса напиши /vote <username>')
        user.next_message_handler = self.chat_handler

    def chat_handler(self, sender, text):
        if text[0:6] == '/vote ':
            if sender.is_voted:
                self.bot.send_message(sender.chat_id, 'Вы уже голосовали! Аляли')
            else:
                username = text[6:]  # '/vote User2' -> 'User2'
                user = find_user_by_username(self.users, username)
                if user:
                    user.votes_number += 1
                    sender.is_voted = True
                    self.bot.send_message(sender.chat_id, 'Ваш голос был учитан')
                else:
                    self.bot.send_message(sender.chat_id, 'Такого игрока не найдено')
        else:
            for user in self.users:
                if user is not sender:
                    self.bot.send_message(user.chat_id, f"--= {sender.username}:\n{text}")

    def night_menu(self, user):
        if user.role == MAFIA:
            self.mafia_night_menu(user)
        elif user.role == CIVILIAN:
            self.civilian_night_menu(user)

    def civilian_night_menu(self, user):
        pass

    def mafia_night_menu(self, user):
        pass
