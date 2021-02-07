import requests
import random
import time
from .Classes.user import User
from .functions import print_structure
from .globals import URL_BASE, TOKEN, URL
from .router import Router


class Bot:
    def __init__(self, token):
        self.token = token
        self.last_update_id = 0
        self.url = f"{URL_BASE}/bot{token}"
        self.users = []
        self.router = Router(self)

    def get_updates(self):
        response = requests.get(f"{self.url}/getUpdates?offset={self.last_update_id + 1}")
        dct = response.json()
        return dct['result']

    def send_message(self, chat_id, text):
        requests.get(f"{self.url}/sendMessage?chat_id={chat_id}&text={text}")

    def run(self):
        while True:
            updates = self.get_updates()
            for update in updates:
                user = self.identify_user(update)
                text: str = update['message']['text']
                self.answer_to_message(user, text)
                self.last_update_id = update['update_id']
            time.sleep(0.5)

    def identify_user(self, update):
        """
        Идентифицирует пользователя по списку пользователей.
        Если пользователя нету, создает новичка
        """
        chat_id = update['message']['chat']['id']
        user = self.find_user(chat_id)
        if user is None:
            user = self.create_user(chat_id)
            self.users.append(user)
        return user

    def find_user(self, chat_id):
        """
        Ищет пользователя в списке пользователей по chat_id.
        Если находит, return user
        Если не находит, return None
        """
        for user in self.users:
            if user.chat_id == chat_id:
                return user
        return None

    def create_user(self, chat_id):
        user = User(chat_id)
        user.next_message_handler = self.start_handler
        return user

    def answer_to_message(self, user, text):
        user.next_message_handler(user, text)

    def start_handler(self, user, text):
        self.send_message(user.chat_id, 'Добро пожаловать в нашего бота! Просим вам зарегистрироваться.\n'
                                        'Введите свой никнейм:')
        user.next_message_handler = self.registration_handler

    def registration_handler(self, user, text):
        username = text.strip()
        if 3 <= len(username) <= 15:
            user.username = username
            self.send_message(user.chat_id, 'Никнейм сохранен!')
            self.main_menu(user)
        else:
            self.send_message(user.chat_id, 'Попробуй еще раз:')

    def main_menu(self, user):
        text = '-----= Главное меню =----\n' \
               f'{user.username} ({user.status})\n' \
               f'Coins: {user.coins}\n' \
               '1 - играть\n' \
               '2 - чихнуть\n' \
               '3 - магазин\n' \
               '4 - удалить аккаунт\n' \
               '5 - тест меню\n' \
               'Ваш выбор:'
        self.send_message(user.chat_id, text)
        user.next_message_handler = self.main_menu_handler

    def main_menu_handler(self, user, text):
        if text == '1':
            pass
        elif text == '2':
            self.send_message(user.chat_id, 'Апчхи!')
        elif text == '3':
            self.store_menu(user)
        elif text == '4':
            pass
        elif text == '5':
            self.test_menu(user)
        else:
            self.send_message(user.chat_id, 'Уважаемый, такой дичи мы не видали')

    def test_menu(self, user):
        text = '---= Тестовое меню =---\n' \
               '0 - назад\n' \
               '1 - тест1\n' \
               '2 - test2\n' \
               '3 - test3\n'
        self.send_message(user.chat_id, text)
        user.next_message_handler = self.test_menu_handler

    def test_menu_handler(self, user, text):
        if text == '0':
            self.main_menu(user)
        elif text == '1':
            self.send_message(user.chat_id, 'Тест 1')
        elif text == '2':
            self.send_message(user.chat_id, 'Тест 2')
        elif text == '3':
            self.send_message(user.chat_id, 'Тест 3')
        else:
            self.send_message(user.chat_id, 'Два говяжа стоят в поле')

    def store_menu(self, user):
        text = '----= Магазин =-----\n' \
               '0 - назад\n' \
               '1 - купить статус серебро (10)\n' \
               '2 - купить статус золото (40)\n' \
               '3 - купить статус VIP (1000)\n' \
               'Ваш выбор:'
        self.send_message(user.chat_id, text)
        user.next_message_handler = self.store_menu_handler

    def store_menu_handler(self, user, text):
        if text == '1':
            if user.coins >= 10:
                user.status = 'серебро'
                self.send_message(user.chat_id, 'Теперь вы серебро!')
                user.coins -= 10
            else:
                self.send_message(user.chat_id, 'Донать!!!')
            self.main_menu(user)
        elif text == '2':
            pass
        elif text == '3':
            pass
        elif text == '0':
            self.main_menu(user)
        else:
            pass
