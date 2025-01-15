from view import View
from model import Model

class Controller:
    def __init__(self):
        self.model = Model()
        self.view = View(self)

    def main(self):
        self.view.main()


if __name__ == '__main__':
    App = Controller()
    App.main()