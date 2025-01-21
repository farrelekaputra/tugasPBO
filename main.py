from view import View
from model import Model

class Controller:
    def __init__(self):
        self.model = Model()
        self.view = View(self)
        self.view.main()

    def main(self):
        self.view.main()

    def exit(self):
        result = self.view.open_messagebox(title="Exit", message="Apakah Anda yakin ingin keluar?")

        if result:
            self.view.destroy()


if __name__ == '__main__':
    App = Controller()
    App.main()