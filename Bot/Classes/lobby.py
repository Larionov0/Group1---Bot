from ..Keyboards.keyboard import Keyboard, Button


class Lobby:
    def __init__(self, id_, name, autor, bot, count=3):
        self.id = id_
        self.name = name
        self.autor = autor
        if autor:
            self.users = [autor]
        else:
            self.users = []
        self.bot = bot
        self.count = count  # нужно юзеров для старта
        self.locked = False

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

        for user in self.users:
            if user is not del_user:
                self.bot.send_message(user.chat_id, f'{del_user.username} покинул лобби')
                self.lobby_menu(user)

    def start_game(self):
        self.locked = True
        for user in self.users:
            self.bot.send_message(user.chat_id, 'Игра началась!')

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
