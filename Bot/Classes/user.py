class User:
    def __init__(self, chat_id, username='Новичок', coins=10, wins=0, looses=0):
        self.chat_id = chat_id
        self.username = username
        self.coins = coins
        self.next_message_handler = None
        self.status = 'дерево'
        self.lobby = None
        self.wins = wins
        self.looses = looses

        self.role = None
        self.votes_number = 0
        self.is_voted = False
        self.is_alive = True

    def __str__(self):
        return f'[-_- {self.username} ({self.status})]'
