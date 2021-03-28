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
        if not user.is_alive:
            return self.looser_menu(user)

        if self.time == DAY:
            self.day_menu(user)
        else:
            self.night_menu(user)

    def looser_menu(self, user):
        self.bot.send_message(user.chat_id, 'Вы мертвы. Наблюдайте.')
        user.next_message_handler = self.looser_menu_handler

    def looser_menu_handler(self, user, text):
        pass

    def get_all_alive_users_str(self):
        text = ''
        for user in self.users:
            if user.is_alive:
                text += f'- {user.username}\n'
        return text

    def day_menu(self, user):
        self.bot.send_message(user.chat_id, 'Сейчас происходит обсуждение.\n'
                                            f'Живые игроки:\n{self.get_all_alive_users_str()}\n'
                                            'Пиши прям сюда.\n'
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
                    self.vote_for_user(sender, user)
                else:
                    self.bot.send_message(sender.chat_id, 'Такого игрока не найдено')
        else:
            for user in self.users:
                if user is not sender:
                    self.bot.send_message(user.chat_id, f"--= {sender.username}:\n{text}")

    def vote_for_user(self, sender, user):
        user.votes_number += 1
        sender.is_voted = True
        self.bot.send_message(sender.chat_id, 'Ваш голос был учитан')

        text = f"😏 {sender.username} проголосовал за {user.username}\n" \
               f"{self.get_votes_str()}"
        self.send_message_to_all_users(text)
        self.check_if_voting_ends()

    def check_if_voting_ends(self):
        result = True
        for user in self.users:
            if not user.is_voted:
                result = False

        if result:
            self.end_voting()

    def end_voting(self):
        max_votes_number: int = max([user.votes_number for user in self.users])
        killed_users = []
        for user in self.users:
            if user.votes_number == max_votes_number:
                user.is_alive = False
                killed_users.append(user)
                self.bot.send_message(user.chat_id, 'Вы были изгнанны!')

        text = 'Изгнанные игроки:\n'
        for user in killed_users:
            text += f'- {user.username}'

        self.send_message_to_all_users(text)
        self.start_night()

    def start_night(self):
        self.time = NIGHT
        self.send_message_to_all_users('🌚 Ночь наступила. Всем спать!')
        for user in self.users:
            self.in_game_menu(user)

    def send_message_to_all_users(self, text):
        for user in self.users:
            self.bot.send_message(user.chat_id, text)

    def get_votes_str(self):
        text = ''
        for user in self.users:
            text += f"{user.username} - {user.votes_number} голосов\n"
        return text

    def night_menu(self, user):
        if user.role == MAFIA:
            self.mafia_night_menu(user)
        elif user.role == CIVILIAN:
            self.civilian_night_menu(user)

    def civilian_night_menu(self, user):
        self.bot.send_message(user.chat_id, 'Ночь. Ты спишь.')
        user.next_message_handler = self.civilian_night_menu_handler

    def civilian_night_menu_handler(self, user, text):
        self.bot.send_message(user.chat_id, 'ТЫ СПИШЬ, Я СКАЗАЛ!')

    def mafia_night_menu(self, user):
        text = 'Выбери юзера на вынос:\n'
        for user in self.users:
            if user.is_alive:
                text += f"- {user.username}\n"

        self.bot.send_message(user.chat_id, text)
        user.next_message_handler = self.mafia_night_menu_handler

    def mafia_night_menu_handler(self, mafia, text):
        user = find_user_by_username(self.users, text)
        if user and user.is_alive:
            user.is_alive = False
            self.send_message_to_all_users(f'{user.username} был убит ночью :(')
            self.start_day()
        else:
            self.bot.send_message(mafia.chat_id, 'Такого юзера нету. Давай по новой.')
            self.mafia_night_menu(mafia)

    def start_day(self):
        self.time = DAY
        self.send_message_to_all_users('🌝 День наступил. Все просыпаемся!')

        for user in self.users:
            user.votes_number = 0
            user.is_voted = False

        for user in self.users:
            self.in_game_menu(user)
