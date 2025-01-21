from repository import Repository

class Model:
    def __init__(self):
        self.repository = Repository()

    def get_all(self):
        return self.repository.get_all()

    def get_by_id(self, music_id):
        return self.repository.get_by_id(music_id)

    def create(self, data):
        return self.repository.create(data)

    def delete_all(self):
        return self.repository.delete_all()

    def delete_by_name(self, name):
        return self.repository.delete_by_name(name)

