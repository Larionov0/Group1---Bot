import requests
import json
import random
import time


def print_structure(struct):
    print(json.dumps(struct, indent=4))


URL_BASE = 'https://api.telegram.org'
TOKEN = '1583405375:AAF3aRNGS_-ksh_cuOeHddQOonlwPZ2F-bA'
URL = f"{URL_BASE}/bot{TOKEN}"


class User:
    def __init__(self, chat_id):
        self.chat_id = chat_id


class Bot:
    def __init__(self, token):
        self.token = token
        self.last_update_id = 0
        self.url = f"{URL_BASE}/bot{token}"
        self.users = []

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
        chat_id = update['message']['chat']['id']
        user = self.find_user(chat_id)
        if user is None:
            user = self.create_user(chat_id)
            self.users.append(user)
        return user

    def find_user(self, chat_id):
        for user in self.users:
            if user.chat_id == chat_id:
                return user
        return None

    def create_user(self, chat_id):
        user = User(chat_id)
        return user

    def answer_to_message(self, user, text):
        self.send_message(user.chat_id, 'Пока в разработке')


bot = Bot(TOKEN)
bot.run()
