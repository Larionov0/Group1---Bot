import requests
import json
import random
import time


def print_structure(struct):
    print(json.dumps(struct, indent=4))


URL_BASE = 'https://api.telegram.org'
TOKEN = '1583405375:AAF3aRNGS_-ksh_cuOeHddQOonlwPZ2F-bA'
URL = f"{URL_BASE}/bot{TOKEN}"


class Bot:
    def __init__(self, token):
        self.token = token
        self.last_update_id = 0
        self.url = f"{URL_BASE}/bot{token}"

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
                self.answer_to_update(update)
                self.last_update_id = update['update_id']
            time.sleep(0.5)

    def answer_to_update(self, update):
        chat_id = update['message']['chat']['id']
        text: str = update['message']['text']

        if 'как дела' in text.lower():
            answer = random.choices(['Хорошо', "Отлично", "Не очень", "Плохо"], [5, 2, 4, 1])[0]
        else:
            answer = text + '!'
        self.send_message(chat_id, answer)


bot = Bot(TOKEN)
bot.run()
