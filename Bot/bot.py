import requests
import random
import time
from .Classes.user import User
from .functions import print_structure
from .globals import URL_BASE, TOKEN, URL
from .router import Router
from .Classes.lobby import Lobby


class Bot:
    def __init__(self, token):
        self.token = token
        self.last_update_id = 0
        self.url = f"{URL_BASE}/bot{token}"
        self.users = []
        self.lobbies = [Lobby('главное', None), Lobby('дополнительное', None, 5)]
        self.router = Router(self)

    def get_updates(self):
        response = requests.get(f"{self.url}/getUpdates?offset={self.last_update_id + 1}")
        dct = response.json()
        return dct['result']

    def send_message(self, chat_id, text, keyboard=None):
        if keyboard:
            keyboard_str = "&reply_markup=" + keyboard.to_json()
        else:
            keyboard_str = '&reply_markup=' + '{"remove_keyboard": true}'
        requests.get(f"{self.url}/sendMessage?chat_id={chat_id}&text={text}{keyboard_str}")

    def run(self):
        while True:
            updates = self.get_updates()
            for update in updates:
                user = self.identify_user(update)
                text: str = update['message']['text']
                self.router.answer_to_message(user, text)
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
        user.next_message_handler = self.router.start_handler
        return user
