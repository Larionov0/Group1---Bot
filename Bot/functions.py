import json


def print_structure(struct):
    print(json.dumps(struct, indent=4))


def find_lobby_by_name(lobbies, name):
    for lobby in lobbies:
        if lobby.name == name:
            return lobby
    return False


def find_lobby_by_id_str(lobbies, id_: str):
    if not id_.isdigit():
        return False
    id_ = int(id_)

    for lobby in lobbies:
        if lobby.id == id_:
            return lobby
    return False


def find_user_by_username(users, username):
    for user in users:
        if user.username == username:
            return user
    return None
