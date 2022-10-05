from tkinter import *

from screens.main_frame import MainFrame
from simulation import CashMachine


class StartupFrame(Frame):
    def __init__(self, master):
        super().__init__(master)

        self.inner_frame = Frame(self, width=80, height=20)

        self.label = Label(
            self.inner_frame,
            text="Número de caixas:",
            width=20,
            font=("arial", 16)
        )

        self.entry = Entry(
            self.inner_frame,
            font=("arial", 16)
        )

        self.button = Button(
            self.inner_frame,
            command=self.on_Go,
            text="Começar"
        )

        self.label.grid(row=0, column=0)
        self.entry.grid(row=0, column=1)
        self.button.grid(row=0, column=2)
        self.inner_frame.pack(anchor=CENTER, expand=True)

    def on_Go(self):
        for i in range(int(self.entry.get())):
            CashMachine(id=i).start()

        frame = MainFrame(self.master)
        self.master.register_frame(frame, "main_frame")
        self.master.swap_frame("main_frame")
