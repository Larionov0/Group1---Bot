from .functions import find_lobby_by_name
from .Keyboards.keyboard import Keyboard, Button


class Router:
    def __init__(self, bot):
        self.bot = bot

    def answer_to_message(self, user, text):
        user.next_message_handler(user, text)

    def start_handler(self, user, text):
        self.bot.send_message(user.chat_id, 'Добро пожаловать в нашего бота! Просим вам зарегистрироваться.\n'
                                        'Введите свой никнейм:')
        user.next_message_handler = self.registration_handler

    def registration_handler(self, user, text):
        username = text.strip()
        if 3 <= len(username) <= 15:
            user.username = username
            self.bot.send_message(user.chat_id, 'Никнейм сохранен!')
            self.main_menu(user)
        else:
            self.bot.send_message(user.chat_id, 'Попробуй еще раз:')

    def main_menu(self, user):
        text = '-----= Главное меню =----\n' \
               f'{user.username} ({user.status})\n' \
               f'Coins: {user.coins}\n' \
               'Ваш выбор:'
        keyboard = Keyboard([
            [Button('Играть'), Button('Чихнуть')],
            [Button('Магазин'), Button('удалить аккаунт')]
        ])
        self.bot.send_message(user.chat_id, text, keyboard)
        user.next_message_handler = self.main_menu_handler

    def main_menu_handler(self, user, text):
        if text == 'Играть':
            self.game_menu(user)
        elif text == 'Чихнуть':
            self.bot.send_message(user.chat_id, 'Апчхи!')
            self.main_menu(user)
        elif text == 'Магазин':
            self.store_menu(user)
        elif text == 'удалить аккаунт':
            pass
        else:
            self.bot.send_message(user.chat_id, 'Уважаемый, такой дичи мы не видали')

    def game_menu(self, user):
        text = '---= Game menu =---\n' \
               '0 - назад\n' \
               '1 - создать лобби\n' \
               '2 - найти лобби\n' \
               '3 - войти в лобби'
        self.bot.send_message(user.chat_id, text)
        user.next_message_handler = self.game_menu_handler

    def game_menu_handler(self, user, text):
        if text == '0':
            self.main_menu(user)
        elif text == '1':
            pass
        elif text == '2':
            self.lobbies_menu(user)
        elif text == '3':
            pass

    def lobbies_menu(self, user):
        text = 'Доступные лобби:\n' \
               '0 - назад\n'
        for lobby in self.bot.lobbies:
            text += f'- {lobby}\n'
        text += 'Выберите лобби по имени: '
        self.bot.send_message(user.chat_id, text)
        user.next_message_handler = self.lobbies_menu_handler

    def lobbies_menu_handler(self, user, text):
        if text == '0':
            return self.game_menu(user)

        lobby = find_lobby_by_name(self.bot.lobbies, text)
        if lobby:
            self.bot.send_message(user.chat_id, 'Такое лобби существует')  # !!!
        else:
            self.bot.send_message(user.chat_id, 'Мы таких не видали:(')

    def store_menu(self, user):
        text = '----= Магазин =-----\n' \
               '0 - назад\n' \
               '1 - купить статус серебро (10)\n' \
               '2 - купить статус золото (40)\n' \
               '3 - купить статус VIP (1000)\n' \
               'Ваш выбор:'
        self.bot.send_message(user.chat_id, text)
        user.next_message_handler = self.store_menu_handler

    def store_menu_handler(self, user, text):
        if text == '1':
            if user.coins >= 10:
                user.status = 'серебро'
                self.bot.send_message(user.chat_id, 'Теперь вы серебро!')
                user.coins -= 10
            else:
                self.bot.send_message(user.chat_id, 'Донать!!!')
            self.main_menu(user)
        elif text == '2':
            pass
        elif text == '3':
            pass
        elif text == '0':
            self.main_menu(user)
        else:
            pass
