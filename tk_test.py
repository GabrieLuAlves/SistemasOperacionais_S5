from tkinter import *


class ScrollableFrame(Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack()

        self.canvas = Canvas(self)
        self.canvas.pack(side=LEFT, fill=BOTH, expand=True)

        self.scroll_bar = Scrollbar(
            self, orient=VERTICAL, command=self.canvas.yview)
        self.scroll_bar.pack(side=RIGHT, fill=Y)
        self.canvas.config(yscrollcommand=self.scroll_bar.set)

        self.internal_frame = Frame(self.canvas)
        self.canvas.create_window(
            (0, 0), window=self.internal_frame, anchor='nw')

        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def __build(self):
        for i in range(300):
            Label(self.internal_frame, text="Olá Mundo! Pela %i vez..." % i).pack()


def add():
    Label(scrollableFrame.internal_frame,
          text=f"Label {scrollableFrame.internal_frame.winfo_height()}").pack()
    scrollableFrame.internal_frame.update_idletasks()


window = Tk()
window.geometry("800x600")

button = Button(window, text="Add text button", command=add)
scrollableFrame = ScrollableFrame(window)

button.place(y=0, relheight=0.1, relwidth=1)
scrollableFrame.place(x=0, rely=0.1, relwidth=1, relheight=0.9)

window.mainloop()
