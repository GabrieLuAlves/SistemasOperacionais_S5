from tkinter import *


class ScrollableFrame(Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack()

        self.canvas = Canvas(self)
        self.canvas.pack(side=LEFT, fill=BOTH)

        self.scroll_bar = Scrollbar(
            self, orient=VERTICAL, command=self.canvas.yview)
        self.scroll_bar.pack(side=RIGHT, fill=Y)
        self.canvas.config(yscrollcommand=self.scroll_bar.set)

        self.internal_frame = Frame(self.canvas)
        self.canvas.create_window(
            (0, 0), window=self.internal_frame, anchor='nw')

        self.canvas.config(scrollregion=self.canvas.bbox("all"))
