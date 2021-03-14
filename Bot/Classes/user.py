class User:
    def __init__(self, chat_id, username='Новичок', coins=10):
        self.chat_id = chat_id
        self.username = username
        self.coins = coins
        self.next_message_handler = None
        self.status = 'дерево'
        self.lobby = None

    def __str__(self):
        return f'[-_- {self.username} ({self.status})]'
