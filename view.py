import tkinter as tk
from tkinter import ttk


class View(tk.Tk):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller

        self.title("Music Player")



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
