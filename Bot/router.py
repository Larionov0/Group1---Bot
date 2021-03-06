from .functions import find_lobby_by_id_str
from .Keyboards.keyboard import Keyboard, Button
from .Classes.lobby import Lobby


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
        keyboard = Keyboard([
            [Button('найти лобби'), Button('войти в лобби')],
            [Button('создать лобби')],
            [Button('назад')]
        ])
        self.bot.send_message(user.chat_id, '---= Game menu =---', keyboard)
        user.next_message_handler = self.game_menu_handler

    def game_menu_handler(self, user, text):
        if text == 'назад':
            self.main_menu(user)
        elif text == 'создать лобби':
            self.create_lobby(user)
        elif text == 'найти лобби':
            self.lobbies_menu(user)
        elif text == 'войти в лобби':
            pass

    def lobbies_menu(self, user):
        text = 'Доступные лобби:\n'
        keyboard = Keyboard([[Button('назад')]])
        for lobby in self.bot.lobbies:
            if lobby.locked is False:
                text += f'- {lobby}\n'
        text += 'Выберите лобби по имени: '
        self.bot.send_message(user.chat_id, text, keyboard)
        user.next_message_handler = self.lobbies_menu_handler

    def lobbies_menu_handler(self, user, text):
        if text == 'назад':
            return self.game_menu(user)

        lobby = find_lobby_by_id_str(self.bot.lobbies, text)
        if lobby:
            self.bot.send_message(user.chat_id, 'Такое лобби существует')  # !!!
            result = lobby.add_user(user)
            if result is False:
                self.bot.send_message(user.chat_id, 'Лобби занято!')
                self.main_menu(user)
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

    def create_lobby(self, user):
        self.bot.send_message(user.chat_id, 'Введите имя для лобби:')
        user.next_message_handler = self.create_lobby_handler

    def create_lobby_handler(self, user, text):
        l = Lobby(self.bot.lobbies, text, user, self.bot)
        self.bot.lobbies.append(l)
        user.lobby = l
        self.bot.send_message(user.chat_id, 'Теперь введите количество людей для старта:')
        user.next_message_handler = self.input_count_for_lobby_handler

    def input_count_for_lobby_handler(self, user, text):
        count = int(text)
        user.lobby.count = count
        self.bot.send_message(user.chat_id, 'Лобби созданно!')
        user.lobby.lobby_menu(user)
