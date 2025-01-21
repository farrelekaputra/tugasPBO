from tkinter import Tk, ttk, messagebox, PhotoImage
from vendor import iconsbase64 as vendor


class View(Tk):
    __MAIN = "assets/icons/IconLogo.png"
    __LOGO = "assets/icons/logo.png"
    __PAUSE = "assets/icons/pause.png"
    __PLAY = "assets/icons/play.png"
    __DEC_VOL = "assets/icons/muted.png"
    __INC_VOL = "assets/icons/notmuted.png"
    __FORWARD = "assets/icons/next.png"
    __BACK = "assets/icons/prev.png"
    __MUSIC = "assets/icons/music.png"
    __FOLDER = "assets/icons/folder.png"
    __SHUFFLE = "assets/icons/shuffle.png"
    __SHUFFLE_ON = "assets/icons/shuffleon.png"
    __REPEAT = "assets/icons/repeat.png"
    __REPEAT_ON = "assets/icons/repeaton.png"
    __LEFT_FRAME = "assets/icons/left_bar.png"
    __RIGHT_FRAME = "assets/icons/right_bar.png"
    __NO_IMAGE = vendor.NOImage

    __TEXT_COLOR = 'white'
    __FRAME_COLOR_THEME = '#131313'
    __FRAME_TEXT_COLOR_THEME = 'white'

    def __init__(self, controller):
        super().__init__()
        self.controller = controller

        self.title("Wave - Music Player")
        self.iconphoto(False, self.__get_images(self.__MAIN))

        self.__center_window()

        self.protocol("WM_DELETE_WINDOW", self.controller.exit)


    def main(self):
        self.mainloop()

    def __center_window(self):
        self.update()

        width = self.winfo_width()
        height = self.winfo_height()

        x_offset = (self.winfo_screenwidth() - width) // 2
        y_offset = (self.winfo_screenheight() - height) // 2

        self.geometry(
            f'{width}x{height}+{x_offset}+{y_offset}'
        )

    @staticmethod
    def open_messagebox(title, message):
        return messagebox.askyesno(
                            title=title,
                            message=message
                        )

    @staticmethod
    def __get_images(image_path):
        return PhotoImage(file=image_path)