import json


class Button:
    def __init__(self, text):
        self.text = text

    def to_dict(self):
        return {'text': self.text}


class Keyboard:
    def __init__(self, buttons):
        self.buttons = buttons

    def to_dict(self):
        objects_matrix = self.buttons
        dicts_matrix = []
        for row in objects_matrix:
            new_row = []
            for button_object in row:
                button_dict = button_object.to_dict()
                new_row.append(button_dict)
            dicts_matrix.append(new_row)

        return {'keyboard': dicts_matrix}

    def to_json(self):
        return json.dumps(self.to_dict(), ensure_ascii=False)


def sample():
    b1 = Button('Играть')
    b2 = Button('Магазин')
    b3 = Button('Выход')

    keyboard = Keyboard([
        [b1, b2],
        [b3]
    ])

    print(keyboard.to_json())

