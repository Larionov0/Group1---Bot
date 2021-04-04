import pickle


class Saver:
    def __init__(self, saving_filename):
        self.saving_filename = saving_filename

    def save(self, lobbies, users):
        with open(self.saving_filename, 'wb') as file:
            pickle.dump({
                'lobbies': lobbies,
                'users': users
            }, file)
        print('Save')

    def load(self):
        with open(self.saving_filename, 'rb') as file:
            dct = pickle.load(file)
        return dct['lobbies'], dct['users']
