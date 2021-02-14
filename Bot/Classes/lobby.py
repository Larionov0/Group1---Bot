class Lobby:
    def __init__(self, name, autor, count=3):
        self.name = name
        self.autor = autor
        if autor:
            self.users = [autor]
        self.count = count  # нужно юзеров для старта

    def __str__(self):
        return f'<{self.name}> ({len(self.users)} / {self.count})'
