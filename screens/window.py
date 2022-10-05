from screens.startup_screen import StartupFrame
from tkinter import *


class Window(Tk):
    def __init__(self):
        super().__init__()

        self.geometry("800x600")

        self.frames = {}
        self.frames["startup_frame"] = StartupFrame(self)

        self.frames["startup_frame"].place(relwidth=1, relheight=1)

    def register_frame(self, frame, name):
        self.frames[name] = frame
        frame.place(relwidth=1, relheight=1)

    def swap_frame(self, frame_name):
        frame = self.frames[frame_name]
        self.tkraise(frame)


def main():
    window = Window()
    window.swap_frame("startup_frame")
    window.mainloop()


if __name__ == "__main__":
    main()
