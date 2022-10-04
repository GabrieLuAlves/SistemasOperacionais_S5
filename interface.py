from threading import Thread
from time import sleep
from tkinter import ttk
import pygame
import pygame.locals as locals


class ProgressBar:
    def __init__(
        self,
        surface,
        left,
        top,
        width,
        height,
        colour=(255, 255, 255),
        finished_colour=(0, 200, 0)
    ):
        self.surface = surface
        self.left = left
        self.top = top
        self.width = width
        self.height = height
        self.colour = colour
        self.finished_colour = finished_colour

    def draw(self, progress):

        if progress >= 100:
            progress = 100
            colour = self.finished_colour
        else:
            colour = self.colour

        bar_colour = (colour)

        pygame.draw.rect(
            self.surface,
            bar_colour,
            pygame.Rect(
                self.left,
                self.top,
                self.width,
                self.height
            ),
            1
        )

        pygame.draw.rect(
            self.surface,
            colour,
            pygame.Rect(
                self.left + 10,
                self.top + 10,
                (self.width - 20) * progress / 100,
                self.height - 20
            )
        )


class Label:
    def __init__(
        self,
        surface=...,
        left=...,
        top=...,
        size=...,
        height=...,
        colour=...,
        background=...,
        text=""
    ):
        self.surface = surface
        self.left = left
        self.top = top
        self.size = size
        self.height = height
        self.colour = colour
        self.background = background
        self.text = text

    def draw(self):
        font = pygame.font.SysFont(None, self.size)
        img = font.render(self.text, True, self.colour, self.background)

        padding_y = (self.height - img.get_height()) / 2

        self.surface.blit(img, (self.left, self.top + padding_y))


class Process(Thread):
    def __init__(self, increment_period):
        super().__init__(name="process")
        self.increment_value = 100 / (increment_period * 10)
        self.progress_bar: ttk.Progressbar = None
        self.value = 0

    def run(self):
        while self.value < 100:
            new_value = self.value + self.increment_value

            if new_value > 100:
                self.value = 100
            else:
                self.value = new_value
            sleep(0.1)


def initial_screen(window):
    pygame.display.flip()


def main():
    window_width = 1024
    window_height = 768

    pygame.init()
    pygame.display.set_caption("Projeto de Sistemas Operacionais")

    window = pygame.display.set_mode((window_width, window_height))
    window.set_colorkey((255, 255, 255))

    margin_left = window_width * (1 - 0.8) / 2
    top = 70
    height = 30
    width = window_width * 0.25
    padding = 10

    distance = height + padding

    label1 = Label(
        surface=window,
        left=margin_left,
        top=top,
        size=24,
        height=height,
        colour=(255, 255, 255),
        background=(50, 50, 50),
        text="Client 1"
    )

    label2 = Label(
        surface=window,
        left=margin_left,
        top=top + distance,
        size=24,
        height=height,
        colour=(255, 255, 255),
        background=(50, 50, 50),
        text="Client 2"
    )

    label3 = Label(
        surface=window,
        left=margin_left,
        top=top + distance * 2,
        size=24,
        height=height,
        colour=(255, 255, 255),
        background=(50, 50, 50),
        text="Client 3"
    )

    label4 = Label(
        surface=window,
        left=margin_left,
        top=top + distance * 3,
        size=24,
        height=height,
        colour=(255, 255, 255),
        background=(50, 50, 50),
        text="Client 4"
    )

    label5 = Label(
        surface=window,
        left=margin_left,
        top=top + distance * 4,
        size=24,
        height=height,
        colour=(255, 255, 255),
        background=(50, 50, 50),
        text="Client 5"
    )

    label6 = Label(
        surface=window,
        left=margin_left,
        top=top + distance * 5,
        size=24,
        height=height,
        colour=(255, 255, 255),
        background=(50, 50, 50),
        text="Client 6"
    )

    progress_bar1 = ProgressBar(
        window,
        margin_left + 100,
        top,
        width,
        height
    )

    progress_bar2 = ProgressBar(
        window,
        margin_left + 100,
        top + distance,
        width,
        height
    )

    progress_bar3 = ProgressBar(
        window,
        margin_left + 100,
        top + distance * 2,
        width,
        height
    )

    progress_bar4 = ProgressBar(
        window,
        margin_left + 100,
        top + distance * 3,
        width,
        height
    )

    progress_bar5 = ProgressBar(
        window,
        margin_left + 100,
        top + distance * 4,
        width,
        height
    )

    progress_bar6 = ProgressBar(
        window,
        margin_left + 100,
        top + distance * 5,
        width,
        height
    )

    process1 = Process(1)
    process2 = Process(2)
    process3 = Process(3)
    process4 = Process(4)
    process5 = Process(5)
    process6 = Process(6)

    process1.start()
    process2.start()
    process3.start()
    process4.start()
    process5.start()
    process6.start()

    client_gui = [
        (label1, progress_bar1, process1),
        (label2, progress_bar2, process2),
        (label3, progress_bar3, process3),
        (label4, progress_bar4, process4),
        (label5, progress_bar5, process5),
        (label6, progress_bar6, process6),
    ]

    while True:
        window.fill((50, 50, 50))

        i = 0
        for label, progress_bar, process in client_gui:
            if process.value < 100:
                label.top = top + distance * i
                progress_bar.top = top + distance * i
                i += 1

                label.draw()
                progress_bar.draw(process.value)

        for event in pygame.event.get():
            if event.type == locals.QUIT:
                pygame.quit()
                exit()

        sleep(0.2)

        pygame.display.update()


if __name__ == "__main__":
    main()
