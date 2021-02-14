import json


def print_structure(struct):
    print(json.dumps(struct, indent=4))


def find_lobby_by_name(lobbies, name):
    for lobby in lobbies:
        if lobby.name == name:
            return lobby
    return False
